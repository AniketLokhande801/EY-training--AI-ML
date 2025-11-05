import langgraph as lg
from stock_data import get_stock_data
from news_fetcher import get_stock_news
from embedding import embed_and_store_news
from chromadb_handler import search_similar_articles
from llm_insights import generate_news_summary, generate_stock_insights
from utils import extract_stock_symbol


# Define the LangGraph workflow using states
class StockInsightsWorkflow(lg.LangGraph):
    def __init__(self, api_keys):
        super().__init__()
        self.api_keys = api_keys
        self.add_state("extract_stock_symbol", self.extract_stock_symbol)
        self.add_state("fetch_stock_data", self.fetch_stock_data)
        self.add_state("fetch_news", self.fetch_news)
        self.add_state("embed_news", self.embed_news)
        self.add_state("similarity_search", self.similarity_search)
        self.add_state("summarize_news", self.summarize_news)
        self.add_state("generate_insights", self.generate_insights)

    def extract_stock_symbol(self, user_query, **kwargs):
        stock_symbol = extract_stock_symbol(user_query)
        return {"stock_symbol": stock_symbol}

    def fetch_stock_data(self, stock_symbol, **kwargs):
        stock_data = get_stock_data(stock_symbol)
        return {"stock_data": stock_data}

    def fetch_news(self, stock_symbol, **kwargs):
        news_articles = get_stock_news(stock_symbol)
        return {"news_articles": news_articles}

    def embed_news(self, news_articles, **kwargs):
        embed_and_store_news(news_articles, kwargs["client"])
        return {"embedded_news": news_articles}

    def similarity_search(self, user_query, **kwargs):
        search_results = search_similar_articles(user_query)
        return {"similar_articles": search_results}

    def summarize_news(self, similar_articles, **kwargs):
        summary = generate_news_summary(similar_articles)
        return {"news_summary": summary}

    def generate_insights(self, stock_data, news_summary, **kwargs):
        insights = generate_stock_insights(stock_data, news_summary)
        return {"insights": insights}
