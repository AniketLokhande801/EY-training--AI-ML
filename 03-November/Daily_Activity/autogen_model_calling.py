import os
from dotenv import load_dotenv
from autogen import AssistantAgent, UserProxyAgent

load_dotenv()

openrouter_api_key = os.getenv('OPENROUTER_API_KEY')

if not openrouter_api_key:
    raise ValueError("OpenRouter API key is not set in the .env file")

assistant = AssistantAgent(
    name="assistant",
    llm_config={
        "config_list": [
            {
                "model": "mistralai/mistral-7b-instruct",  # or another OpenRouter model
                "api_key": openrouter_api_key,
                "base_url": "https://openrouter.ai/api/v1",  # critical for OpenRouter
                "price": [0.25, 0.25]
            }
        ]
    }
)

user_proxy = UserProxyAgent(name="user_proxy", human_input_mode="NEVER",code_execution_config={"use_docker": False})

user_proxy.initiate_chat(
    assistant,
    message="What's the capital of France?"
)
