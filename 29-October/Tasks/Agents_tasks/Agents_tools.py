import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env file")

# Initialize the Mistral model via OpenRouter
llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    temperature=0.4,
    max_tokens=256,
    api_key=api_key,
    base_url=base_url,
)


memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


def summarize(text: str) -> str:
    prompt = f"Summarize the following text in a concise way: {text}"
    return llm.invoke(prompt).content

def analyze_sentiment(text: str) -> str:
    prompt = f"Analyze the sentiment of the following text: {text}"
    return llm.invoke(prompt).content


notes = []

def store_note(note: str) -> str:
    notes.append(note)
    return f"Noted: '{note}'"

def get_notes() -> str:
    if not notes:
        return "You have no notes."
    return f"You currently have {len(notes)} note(s): " + ", ".join(notes)


def improve_text(text: str) -> str:
    prompt = f"Rewrite the following text to make it clearer and more professional: {text}"
    return llm.invoke(prompt).content

def classify_priority(task: str) -> str:
    prompt = f"Classify the urgency of the following task: {task}"
    return llm.invoke(prompt).content



print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        print("\nConversation ended.")
        break

    if user_input.lower().startswith("summarize"):
        text = " ".join(user_input.split()[1:])
        summary = summarize(text)
        print("Tool:", summary)
        memory.save_context({"input": user_input}, {"output": summary})
        continue

    if user_input.lower().startswith("analyze"):
        text = " ".join(user_input.split()[1:])
        sentiment = analyze_sentiment(text)
        print("Tool:", sentiment)
        memory.save_context({"input": user_input}, {"output": sentiment})
        continue

    if user_input.lower().startswith("note"):
        note = " ".join(user_input.split()[1:])
        note_response = store_note(note)
        print("Tool:", note_response)
        memory.save_context({"input": user_input}, {"output": note_response})
        continue

    if user_input.lower() == "get notes":
        notes_response = get_notes()
        print("Tool:", notes_response)
        memory.save_context({"input": user_input}, {"output": notes_response})
        continue

    if user_input.lower().startswith("improve"):
        text = " ".join(user_input.split()[1:])
        improved_text = improve_text(text)
        print("Tool:", improved_text)
        memory.save_context({"input": user_input}, {"output": improved_text})
        continue

    if user_input.lower().startswith("priority"):
        task = " ".join(user_input.split()[1:])
        priority = classify_priority(task)
        print("Tool:", priority)
        memory.save_context({"input": user_input}, {"output": priority})
        continue
    try:
        response = llm.invoke(user_input)
        print("Agent:", response.content)
        memory.save_context({"input": user_input}, {"output": response.content})
    except Exception as e:
        print("Error:", e)