from autogen import AssistantAgent
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY missing in .env")

# LLM configuration for both agents
llm_config = {
    "model": "meta-llama/llama-3-8b-instruct",
    "api_key": api_key,
    "base_url": base_url,
    "temperature": 0.7,
    "max_tokens": 700,
}

# Create Assistant agents
researcher = AssistantAgent(
    name="Researcher",
    llm_config=llm_config,
    system_message="You are a research assistant. Research the given topic and provide factual, clear insights in about 10 concise bullet points.",
)

summarizer = AssistantAgent(
    name="Summarizer",
    llm_config=llm_config,
    system_message="You are a summarizer. Create a short summary (3–5 sentences) and 5 key bullet points from the given research notes.",
)


# Notifier function to log summaries
def notifier_agent(summary: str, filename: str = "summary_log.txt"):
    # Log the summary to the file
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} - AUTOGEN: Notified and saved to {filename}\n")
        f.write(f"{summary}\n\n")

    print("Summary has been logged.")
    return {}


# Research pipeline
def run_pipeline(topic: str):
    # Research the topic
    research = researcher.generate_reply(
        messages=[{"role": "user", "content": f"Research this topic: {topic}"}]
    )
    # Summarize the research
    summary = summarizer.generate_reply(
        messages=[{"role": "user", "content": f"Summarize this research:\n{research}"}]
    )
    print("Agent (Summary):", summary)
    # Log the summary
    notifier_agent(summary)


# Main loop for user interaction
if __name__ == "__main__":
    print("\n=== Start chatting with your Agent ===")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            print("\nConversation ended.")
            break

        # Research flow based on user input
        if user_input.lower().startswith("research"):
            topic = user_input.replace("research", "").strip()
            if not topic:
                print("Agent: Please specify a topic.")
                continue
            try:
                print(f"Agent: Researching the topic: '{topic}'...")
                run_pipeline(topic)
            except Exception as e:
                print("Agent: Error during research flow:", e)
            continue

        # If input doesn't match 'research' command, it could be handled differently if needed
        else:
            print("Agent: I can help with research. Type 'research <your topic>' to get started.")
