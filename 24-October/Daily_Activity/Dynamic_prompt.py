import os
import json
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ----------------------------------------------------------
# 1. Load environment variables
# ----------------------------------------------------------
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY missing in .env")

# ----------------------------------------------------------
# 2. Initialize model (Mistral via OpenRouter)
# ----------------------------------------------------------
llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    temperature=0.7,
    max_tokens=256,
    api_key=api_key,
    base_url=base_url
)

# Define tools that can be used
tools = [{
    "type": "function",
    "function": {
        "name": "search_topic",
        "description": "Search for additional information about a topic",
        "parameters": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "The topic to search for"
                }
            },
            "required": ["topic"]
        }
    }
}]


# ----------------------------------------------------------
# 3. Define a dynamic ChatPromptTemplate
# ----------------------------------------------------------
prompt = ChatPromptTemplate.from_template(
    "<s>[INST] You are a concise assistant. Use available tools if needed to explain {topic} in simple terms for a beginner. [/INST]"
)


# Output parser converts model output to plain string
parser = StrOutputParser()


# 4 creating reusable method

def generate_explanation(topic):
    chain = prompt | llm | parser
    response = chain.invoke({
        "topic": topic,
        "tools": tools,
        "tool_choice": "auto"
    })
    return response



# run dynamically for the topic
user_input = input("What is you topic:  ").strip()
response = generate_explanation(user_input)
print("\n response by the model : ")
print(response)

# 6 Log the prompts
os.makedirs("logs", exist_ok=True)
log_entry = {
    "timestamp": datetime.utcnow().isoformat(),
    "topic": user_input,
    "response": response,
}

with open("logs/prompt_template_log.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(log_entry) + "\n")

print("\n response logged to log file ")