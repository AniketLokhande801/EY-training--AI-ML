from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from langchain.messages import SystemMessage
from langchain_core.messages import HumanMessage

import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

# Initialize FastAPI app
app = FastAPI()

# HTML templates folder
templates = Jinja2Templates(directory="templates")

# Initialize LLM
llm = ChatOpenAI(
    model="meta-llama/llama-3-8b-instruct",
    temperature=0.4,
    max_tokens=512,
    api_key=api_key,
    base_url=base_url,
)

HISTORY_FILE = "QA_history.json"



def save_to_history(user_query: str, llm_response: str):
    data = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = []
    data.append({"user_query": user_query, "llm_response": llm_response})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)



@app.api_route("/", methods=["GET", "POST"], response_class=HTMLResponse)
async def chat(request: Request, query: str = Form(None)):
    result = None

    if request.method == "POST" and query:
        try:
            # Call the LLM
            response_obj = llm.invoke(
                [
                    SystemMessage(content="You are a helpful assistant."),
                    HumanMessage(content=query)
                ]
            )
            # llm_output = getattr(response_obj, "content", str(response_obj))

            # Save to history
            save_to_history(query, response_obj.content)
            result = response_obj.content
            print(result)

        except Exception as e:
            result = f"Error: {str(e)}"

    # Render page (both GET and POST)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "query": query,
        "result": result    })
