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
    # max_tokens=256,
    api_key=api_key,
    base_url=base_url,
)

# ----------------------------------------------------------
# 3. Define dynamic ChatPromptTemplate for summary and quiz
# ----------------------------------------------------------
prompt_summary = ChatPromptTemplate.from_template(
    "<s>[INST] You are a short concise assistant. Summarize {topic} in simple terms. [/INST]"
)

prompt_quiz = ChatPromptTemplate.from_template(
    "<s>[INST] Generate the  (3)Three question Quiz on the {summary} with MCQ and answers at the end. [/INST]"
)

# Output parser converts model output to plain string
parser = StrOutputParser()

# ----------------------------------------------------------
# 4. Reusable methods for generating summary and quiz
# ----------------------------------------------------------
def generate_summary(topic):
    chain = prompt_summary | llm | parser
    response = chain.invoke({"topic": topic})
    return response

def generate_quiz(summary):
    chain = prompt_quiz | llm | parser
    response = chain.invoke({"summary": summary})
    return response

# ----------------------------------------------------------
# 5. Run the flow for the given topic
# ----------------------------------------------------------
user_input = input("What is your topic: ").strip()

# Generate the summary
summary_response = generate_summary(user_input)
print("\nSummary of the Topic: ")
print(summary_response)

# Generate the quiz questions based on the summary
quiz_response = generate_quiz(summary_response)
print("\nQuiz on the Topic: ")
print(quiz_response)

# ----------------------------------------------------------
# 6. Log the responses (summary and quiz)
# ----------------------------------------------------------
os.makedirs("logs", exist_ok=True)

log_entry = {
    "timestamp": datetime.utcnow().isoformat(),
    "topic": user_input,
    "summary": summary_response,
    "quiz": quiz_response,
}

# Write log entry to JSONL file
with open("logs/sequential_chaining.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(log_entry) + "\n")

print("\nResponses logged to log file.")