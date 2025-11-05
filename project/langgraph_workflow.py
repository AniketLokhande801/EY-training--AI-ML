from langgraph.graph import StateGraph
from pydantic import BaseModel

from modules.stock_data import get_stock_data
from modules.news_fetcher import get_stock_news
from modules.embedding import embed_and_store_news
from modules.chromadb_handler import search_similar_articles
from modules.llm_insights import generate_news_summary, generate_stock_insights
from modules.utils import extract_stock_symbol
from modules.sentiment_analyzer import SentimentAnalyzer

# Define the state schema
class StockWorkflowState(BaseModel):
    user_query: str
    stock_symbol: str = None
    stock_data: list[dict] = None
    news_articles: list = None
    embedded_news: list = None
    similar_articles: list = None
    news_summary: str = None
    insights: str = None
    sentiment_analyzed_articles: list = None

# Define state functions
def extract_symbol(state: StockWorkflowState):
    symbol = extract_stock_symbol(state.user_query)
    return {"stock_symbol": symbol}

def fetch_data(state: StockWorkflowState):
    data = get_stock_data(state.stock_symbol)
    if not data:
        raise ValueError(f"No stock data found for symbol: {state.stock_symbol}")
    return {"stock_data": data}


def fetch_news(state: StockWorkflowState):
    articles = get_stock_news(state.stock_symbol)
    return {"news_articles": articles}

def embed_news(state: StockWorkflowState):
    embed_and_store_news(state.news_articles)  # Replace `None` with actual client if needed
    return {"embedded_news": state.news_articles}

def search_similar(state: StockWorkflowState):
    results = search_similar_articles(state.user_query)
    return {"similar_articles": results}

def summarize(state: StockWorkflowState):
    summary = generate_news_summary(state.similar_articles)
    return {"news_summary": summary}

def generate_insights(state: StockWorkflowState):
    insights = generate_stock_insights(state.stock_data, state.news_summary)
    return {"insights": insights}

sentiment_analyzer = SentimentAnalyzer()

def analyze_sentiment(state: StockWorkflowState):
    # Analyze sentiment of the news articles
    articles_with_sentiment = sentiment_analyzer.analyze_articles(state.news_articles)
    return {"sentiment_analyzed_articles": articles_with_sentiment}

# Build the graph
graph = StateGraph(StockWorkflowState)

# Add states
graph.add_node("extract_stock_symbol", extract_symbol)
graph.add_node("fetch_stock_data", fetch_data)
graph.add_node("fetch_news", fetch_news)
graph.add_node("embed_news", embed_news)
graph.add_node("similarity_search", search_similar)
graph.add_node("summarize_news", summarize)
graph.add_node("generate_insights", generate_insights)
graph.add_node("analyze_sentiment", analyze_sentiment)


# Define transitions
graph.set_entry_point("extract_stock_symbol")
graph.add_edge("extract_stock_symbol", "fetch_stock_data")
graph.add_edge("fetch_stock_data", "fetch_news")
graph.add_edge("fetch_news", "analyze_sentiment")
graph.add_edge("analyze_sentiment", "embed_news")
graph.add_edge("embed_news", "similarity_search")
graph.add_edge("similarity_search", "summarize_news")
graph.add_edge("summarize_news", "generate_insights")

# Compile the workflow
workflow = graph.compile()
