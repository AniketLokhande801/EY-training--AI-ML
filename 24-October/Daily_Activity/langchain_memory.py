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
    base_url=base_url,
)

# ----------------------------------------------------------
# 3. Define dynamic ChatPromptTemplate for conversation
# ----------------------------------------------------------
prompt_conversation = ChatPromptTemplate.from_template(
    "<s>[INST] You are a helpful assistant. Respond based on the following conversation: {conversation_history} User: {user_input} [/INST]"
)

# Output parser converts model output to plain string
parser = StrOutputParser()


# ----------------------------------------------------------
# 4. Function to handle sequential conversation with memory
# ----------------------------------------------------------
def handle_conversation(conversation_history, user_input):
    # Create a chain with the prompt template, model, and parser
    chain = prompt_conversation | llm | parser

    # Pass the entire conversation history and the new user input into the chain
    conversation_input = {
        "conversation_history": conversation_history,
        "user_input": user_input,
    }

    # Generate the model's response based on the entire conversation
    response = chain.invoke(conversation_input)

    # Update the conversation history with the new user input and the model's response
    conversation_history += f"User: {user_input}\nAssistant: {response}\n"

    return response, conversation_history


# ----------------------------------------------------------
# 5. Main loop for the conversation
# ----------------------------------------------------------
def start_conversation():
    conversation_history = ""  # Empty string to hold conversation history

    while True:
        # Take user input
        user_input = input("You: ").strip()

        # Exit condition
        if user_input.lower() == "exit":
            print("Exiting the chat. Goodbye!")
            break

        # Get the assistant's response and update the conversation history
        response, conversation_history = handle_conversation(conversation_history, user_input)

        # Display the assistant's response
        print(f"Assistant: {response}")

        # Log the conversation (optional)
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "conversation_history": conversation_history,
        }

        # Append to log file
        os.makedirs("logs", exist_ok=True)
        with open("logs/conversation_log.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")


# ----------------------------------------------------------
# 6. Start the conversation
# ----------------------------------------------------------
if __name__ == "__main__":
    start_conversation()