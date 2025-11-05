from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the Gemini API Key from the environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini LLM (Google Generative AI)
import os
import requests
import yfinance as yf
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.api.types import Documents, Embeddings
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=GEMINI_API_KEY)

# Initialize embedding model and ChromaDB
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.PersistentClient(path="./chroma_store")
collection = chroma_client.get_or_create_collection(name="stock_news")

# LangGraph state
class State(dict):
    pass

# Node: Extract stock name
def extract_stock_name(state: State) -> State:
    query = state["user_query"]
    prompt = f"Extract only the company or stock ticker from this query: '{query}'"
    response = llm.invoke([HumanMessage(content=prompt)])
    state["stock_name"] = response.content.strip()
    return state

# Node: Fetch stock data
def fetch_stock_data(state: State) -> State:
    ticker = state["stock_name"]
    stock = yf.Ticker(ticker)
    hist = stock.history(period="7d")
    current_price = stock.info.get("currentPrice", None)
    state["stock_data"] = {
        "ticker": ticker,
        "price": current_price,
        "history": hist.to_dict()
    }
    return state

# Node: Fetch news
def fetch_news(state: State) -> State:
    ticker = state["stock_name"]
    url = f"https://newsapi.org/v2/everything?q={ticker}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    articles = response.json().get("articles", [])[:10]
    state["articles"] = articles
    return state

# Node: Embed news
def embed_news(state: State) -> State:
    articles = state["articles"]
    texts = [f"{a['title']}. {a.get('description', '')}" for a in articles]
    embeddings = embed_model.encode(texts)
    state["embedded_articles"] = list(zip(texts, embeddings))
    return state

# Node: Store embeddings
def store_embeddings(state: State) -> State:
    for i, (text, embedding) in enumerate(state["embedded_articles"]):
        collection.add(documents=Documents([text]), embeddings=Embeddings([embedding]), ids=[f"doc_{i}"])
    return state

# Node: Semantic search
def search_news(state: State) -> State:
    query_embedding = embed_model.encode([state["user_query"]])[0]
    results = collection.query(query_embeddings=[query_embedding], n_results=3)
    state["relevant_articles"] = results["documents"][0]
    return state

# Node: Summarize news
def summarize_news(state: State) -> State:
    joined = "\n\n".join(state["relevant_articles"])
    prompt = f"Summarize the following news articles into 5 bullet points:\n\n{joined}"
    response = llm.invoke([HumanMessage(content=prompt)])
    state["news_summary"] = response.content.strip()
    return state

# Node: Generate insight
def generate_insight(state: State) -> State:
    prompt = f"""Based on the following 7-day stock data and news summary, provide a concise insight and a recommendation (buy, hold, sell):

Stock Data: {state['stock_data']}
News Summary: {state['news_summary']}
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    state["final_insight"] = response.content.strip()
    return state

# Build LangGraph
graph = StateGraph(State)
graph.add_node("ExtractStock", extract_stock_name)
graph.add_node("FetchStockData", fetch_stock_data)
graph.add_node("FetchNews", fetch_news)
graph.add_node("EmbedNews", embed_news)
graph.add_node("StoreEmbeddings", store_embeddings)
graph.add_node("SearchNews", search_news)
graph.add_node("SummarizeNews", summarize_news)
graph.add_node("GenerateInsight", generate_insight)

graph.set_entry_point("ExtractStock")
graph.add_edge("ExtractStock", "FetchStockData")
graph.add_edge("ExtractStock", "FetchNews")
graph.add_edge("FetchNews", "EmbedNews")
graph.add_edge("EmbedNews", "StoreEmbeddings")
graph.add_edge("ExtractStock", "SearchNews")
graph.add_edge("SearchNews", "SummarizeNews")
graph.add_edge("SummarizeNews", "GenerateInsight")
graph.add_edge("FetchStockData", "GenerateInsight")
graph.add_edge("GenerateInsight", END)

app = graph.compile()

# Run the graph
if __name__ == "__main__":
    user_query = "What are the insights about Infosys?"
    final_state = app.invoke({"user_query": user_query})
    print("\n✅ Final Insight:")
    print(final_state["final_insight"])


# Function to generate 5-bullet-point summary of news articles using LLM
def generate_news_summary(news_articles):
    article_text = "\n\n".join([f"Title: {article['title']}\nContent: {article['content']}" for article in news_articles])
    prompt = f"""
    Summarize the following news articles in 5 concise bullet points:
    {article_text}
    """
    response = llm.invoke(prompt)
    return response.content

# Function to generate stock insights using LLM
def generate_stock_insights(stock_data, news_summary):
    prompt = f"""
    Here is the 7-day stock data and news summary . 
    Please generate a short response summarizing the stock's outlook and suggest an action (buy, hold, sell) based on the data and news.

    Stock Data: {stock_data}
    News Summary: {news_summary}
    """
    response = llm.invoke(prompt)
    return response.content
