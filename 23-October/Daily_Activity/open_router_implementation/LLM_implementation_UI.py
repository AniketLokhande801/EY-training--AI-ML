import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import SecretStr


load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY1")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")


api_key = SecretStr(api_key) if api_key else None

if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env file")


llm = ChatOpenAI(
    model="x-ai/grok-code-fast-1",  # Ensure this is a valid model
    temperature=0.3,
    max_tokens=100,
    api_key=api_key,
    base_url=base_url,
)


st.set_page_config(page_title="Chatbot")


system_message = SystemMessage(content="You are a helpful and concise AI assistant.")


def get_bot_response(user_input):

    messages = [
        system_message,
        HumanMessage(content=f"<s>[INST] {user_input} [/INST]")
    ]

    try:

        response = llm.invoke(messages)
        bot_message = response.content.strip() or "(no content returned)"
        return bot_message
    except Exception as e:
        return f"Error: {str(e)}"


st.title("LLM App")

user_input = st.text_input("You:", "")

if user_input:

    bot_response = get_bot_response(user_input)


    st.write(f"**You**: {user_input}")
    st.write(f"**AI**: {bot_response}")


    st.text_input("You:", "", key="input_box")
