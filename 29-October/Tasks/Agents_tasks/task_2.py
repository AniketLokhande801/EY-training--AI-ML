import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage


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




def count_words(text: str) -> str:
    word_count = len(text.split())
    return f"Your sentence has {word_count} words."


def reverse_text(text: str) -> str:
    reversed_text = " ".join(text.split()[::-1])
    return f"Reversed sentence: {reversed_text}"


def define_word(word: str) -> str:
    prompt = f"Define the word '{word}' or give a synonym."
    return llm.invoke(prompt).content


def convert_case(text: str, to_upper: bool) -> str:
    if to_upper:
        return text.upper()
    else:
        return text.lower()


def repeat_word(word: str, count: int) -> str:
    return " ".join([word] * count)


def show_history() -> str:
    messages = memory.load_memory_variables({}).get("chat_history", [])

    if not messages:
        return "No history available."

    history = []

    for msg in messages:
        if isinstance(msg, HumanMessage):
            history.append(f"You: {msg.content}")
        elif isinstance(msg, AIMessage):
            history.append(f"Agent: {msg.content}")

    return "\n".join(history)




print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ").strip()

    if user_input.lower() == "exit":
        print("\nConversation ended.")
        break

    if user_input.lower().startswith("count"):
        text = " ".join(user_input.split()[1:])
        word_count = count_words(text)
        print("Tool:", word_count)
        memory.save_context({"input": user_input}, {"output": word_count})
        continue

    if user_input.lower().startswith("reverse"):
        text = " ".join(user_input.split()[1:])
        reversed_sentence = reverse_text(text)
        print("Tool:", reversed_sentence)
        memory.save_context({"input": user_input}, {"output": reversed_sentence})
        continue

    # 3. Vocabulary Helper Command
    if user_input.lower().startswith("define"):
        word = user_input.split()[1].strip()
        definition = define_word(word)
        print("Tool:", definition)
        memory.save_context({"input": user_input}, {"output": definition})
        continue

    if user_input.lower().startswith("upper"):
        text = " ".join(user_input.split()[1:])
        upper_text = convert_case(text, to_upper=True)
        print("Tool:", upper_text)
        memory.save_context({"input": user_input}, {"output": upper_text})
        continue

    if user_input.lower().startswith("lower"):
        text = " ".join(user_input.split()[1:])
        lower_text = convert_case(text, to_upper=False)
        print("Tool:", lower_text)
        memory.save_context({"input": user_input}, {"output": lower_text})
        continue

    if user_input.lower().startswith("repeat"):
        parts = user_input.split()
        word = parts[1]
        try:
            count = int(parts[2])
            repeated = repeat_word(word, count)
            print("Tool:", repeated)
            memory.save_context({"input": user_input}, {"output": repeated})
        except ValueError:
            print("Tool: Please specify a valid number for repetition.")
        continue

    if user_input.lower() == "history":
        history = show_history()
        print("Tool:", history)
        continue

    # Default: Use LLM for other commands
    try:
        response = llm.invoke(user_input)
        print("Agent:", response.content)
        memory.save_context({"input": user_input}, {"output": response.content})
    except Exception as e:
        print("Error:", e)