from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
import os
from typing import TypedDict

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY missing in .env")

llm = ChatOpenAI(
    model="meta-llama/llama-3-8b-instruct",
    temperature=0.7,
    max_tokens=512,
    api_key=api_key,
    base_url=base_url,
)


class ResearchState(TypedDict):
    topic: str
    research: str
    summary: str


def Researcher(state: ResearchState):
    msg = [
        SystemMessage(
            content="You are a research assistant. Research the given topic in detail and return 10 bullet points."),
        HumanMessage(content=f"Topic: {state['topic']}")
    ]
    result = llm.invoke(msg).content

    print(f"Topic: {state['topic']}")
    print("Researching...")
    return {"research": result}


def Summarizer(state: ResearchState):
    msg = [
        SystemMessage(
            content="You are a summarizer. Summarize the given research into a short paragraph and 5 key bullet points."),
        HumanMessage(content=state["research"])
    ]
    result = llm.invoke(msg).content
    print(f"Suammary: {result}")
    return {"summary": result}


def Notifier(summary: str, filename: str = "summary_log.txt"):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"LangGraph:- Notified and saved to {filename}")
        print("Notified")
    return {}


graph = StateGraph(ResearchState)
graph.add_node("Researcher", Researcher)
graph.add_node("Summarizer", Summarizer)
graph.add_node("Notifier", Notifier)

graph.add_edge(START, "Researcher")
graph.add_edge("Researcher", "Summarizer")
graph.add_edge("Summarizer", "Notifier")
graph.add_edge("Notifier", END)

workflow = graph.compile(checkpointer=InMemorySaver())
config = {"configurable": {"thread_id": "1"}}

initial_state = {"topic": "Impact of Artificial Intelligence on Healthcare"}
workflow.invoke(initial_state, config)