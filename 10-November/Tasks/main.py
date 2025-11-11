from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os, re, logging


load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = "https://openrouter.ai/api/v1"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)


app = FastAPI(title="LangGraph Query Router API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to specific domains
    allow_methods=["*"],
    allow_headers=["*"],
)


llm = ChatOpenAI(
    model="meta-llama/llama-3-8b-instruct",
    temperature=0.4,
    max_tokens=512,
    api_key=api_key,
    base_url=base_url,
)


class QueryParse(BaseModel):
    task: str = Field(..., description="Type of task e.g. math, date, reverse, default")
    query: str = Field(..., description="Original user query")


class QueryRequest(BaseModel):
    query: str


def parse_query_with_llm(state: dict):
    query = state.get("query")
    logging.info(f"User query received: {query}")

    structured_llm = llm.with_structured_output(QueryParse)
    structured_output = structured_llm.invoke(
        f"""Classify this query into one of the following task types:
    - "math": for math operations like add, subtract, multiply, divide
    - "date": for questions about today's date or time
    - "reverse": for reversing a string
    - "default": for anything else

    Respond with a single JSON object like:
    {{"task": "math", "query": "add 5 and 4"}}

    Query: {query}
    """
    )

    parsed = structured_output.dict()
    logging.info(f"Parsed LLM output: {parsed}")
    return parsed


def do_math(state: dict):
    query = state.get("query")
    logging.info(f"Executing math operation: {query}")

    numbers = [int(num) for num in re.findall(r'\d+', query)]
    result = None

    if "add" in query or "sum" in query or "plus" in query:
        result = sum(numbers)
    elif "subtract" in query or "minus" in query:
        result = numbers[0] - numbers[1] if len(numbers) >= 2 else "Invalid input"
    elif "multiply" in query or "times" in query:
        result = numbers[0] * numbers[1] if len(numbers) >= 2 else "Invalid input"
    elif "divide" in query or "by" in query:
        result = numbers[0] / numbers[1] if len(numbers) >= 2 and numbers[1] != 0 else "Invalid input"
    else:
        result = "Math operation not recognized"

    logging.info(f"Math result: {result}")
    return {"result": f"Math result: {result}"}


def do_date(state: dict):
    query = state.get("query")
    logging.info(f"Executing date operation: {query}")

    date_prompt = (
        f"You are a helpful assistant. Answer the user's question about dates or time.\n"
        f"Today's date is {datetime.now().strftime('%Y-%m-%d')}.\n"
        f"User query: {query}"
    )

    response = llm.invoke(date_prompt)
    logging.info(f"Date response: {response.content}")
    return {"result": response.content}


def do_reverse(state: dict):
    query = state.get("query")
    logging.info(f"Executing string reversal: {query}")
    text = re.sub(r'reverse\s+(the\s+word\s+)?', '', query, flags=re.IGNORECASE).strip()
    reversed_text = text[::-1]
    return {"result": f"Reversed string: {reversed_text}"}


def default_response(state: dict):
    query = state.get("query")

    logging.info(f"Executing default response for: {query}")
    return {"result": "Sorry, I couldn't understand your query."}


builder = StateGraph(dict)
builder.add_node("parse", parse_query_with_llm)
builder.add_node("math", do_math)
builder.add_node("date", do_date)
builder.add_node("reverse", do_reverse)
builder.add_node("default", default_response)

def route(state: dict):
    return state["task"]

builder.add_conditional_edges("parse", route, {
    "math": "math",
    "date": "date",
    "reverse": "reverse",
    "default": "default"
})

builder.set_entry_point("parse")
graph = builder.compile()


@app.post("/process_query")
async def process_query(req: QueryRequest):
    try:
        result = graph.invoke({"query": req.query})
        logging.info(f"Final result: {result}")
        return {"result": result.get("result", "No result found.")}
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return {"result": f"Error: {str(e)}"}
