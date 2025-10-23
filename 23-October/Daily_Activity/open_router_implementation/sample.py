# import os
# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
# from langchain_core.messages import SystemMessage, HumanMessage
#
# # 1. Load environment variables from .env
# load_dotenv()
#
# api_key = os.getenv("OPENROUTER_API_KEY")
# base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
# # print(api_key)
# if not api_key:
#     raise ValueError("OPENROUTER_API_KEY not found in .env file")
#
# # 2. Initialize LangChain model pointing to OpenRouter
# llm = ChatOpenAI(
#     # model="mistralai/mistral-7b-instruct",
#     model="x-ai/grok-code-fast-1",
#     temperature=0.7,
#     max_tokens=256,
#     api_key=api_key,
#     base_url=base_url,
# )
#
# # 3. Define messages (Mistral models work better with [INST]...[/INST])
# messages = [
#     SystemMessage(content="You are a helpful and concise AI assistant."),
#     HumanMessage(content="<s>[INST] Explain in simple terms how convolutional neural networks work. [/INST]"),
# ]
#
# # 4. Invoke model and print response
# try:
#     response = llm.invoke(messages)
#     print("Assistant:", response.content.strip() or "(no content returned)")
# except Exception as e:
#     print("Error:", e)



import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import SecretStr

# 1. Load environment variables from .env
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY1")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

# 2. Wrap the API key in SecretStr for security
api_key = SecretStr(api_key) if api_key else None
# Debugging line to ensure API key is loaded
print("API Key:", api_key)

if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env file")

# 2. Initialize LangChain model pointing to OpenRouter
llm = ChatOpenAI(
    model="x-ai/grok-code-fast-1",  # Ensure this is a valid model
    temperature=0.7,
    max_tokens=256,
    api_key=api_key,
    base_url=base_url,
)

# 3. Define messages (Mistral models work better with [INST]...[/INST])
messages = [
    SystemMessage(content="You are a helpful and concise AI assistant."),
    HumanMessage(content="<s>[INST] Explain in simple terms how convolutional neural networks work. [/INST]"),
]

# 4. Invoke model and print response
try:
    response = llm.invoke(messages)
    print("Assistant:", response.content.strip() or "(no content returned)")
except Exception as e:
    if "402" in str(e):  # Checking for insufficient credits error
        print("Error: Insufficient credits. Please purchase credits at https://openrouter.ai/settings/credits.")
    else:
        print("Error:", e)

