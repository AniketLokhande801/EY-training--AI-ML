# Stock Insights Chatbot with Sentiment Analysis

This project is an interactive stock insights chatbot built with LangGraph. It fetches stock data and related news, performs sentiment analysis on news articles using finBERT, and generates AI-driven stock insights.

## Features

- **Extracts stock symbols** from user queries.
- **Fetches historical stock price data**.
- **Retrieves the latest news articles** related to the stock symbol.
- **Performs financial sentiment analysis** on news articles with finBERT.
- **Summarizes news and generates stock insights** using AI.
- **Intuitive chat-style user interface** built with Streamlit.

## Getting Started

### Prerequisites

- Python 3.8+
- API keys:
  - **NewsAPI key** for news retrieval.
  - **Gemini API** for LLM intergration
  - **Optional:** Any additional API keys for stock data .
### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/AniketLokhande801/EY-training--AI-ML.git
    cd stock-insights-chatbot
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use 'venv\Scripts\activate'
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up your `.env` file in the root directory with:

    ```text
    NEWSAPI_KEY=your_newsapi_key_here
    GEMINI_API_KEY=your_optional_stock_api_key_here
    ```

### Usage

1. Start the Streamlit app:

    ```bash
    streamlit run app.py
    ```

2. This will launch a web interface where you can enter stock-related questions and receive data, news summaries, sentiment analysis, and AI insights.

## Project Structure

- **`app.py`**: Main Streamlit app and workflow integration.
- **`modules/`**: Contains modules like stock data fetcher, news fetcher, sentiment analyzer, and LangGraph workflow.
- **`requirements.txt`**: Python dependencies.

## Dependencies

Key dependencies include:

- `streamlit` for UI.
- `langgraph` for workflow orchestration.
- `transformers` and `torch` for sentiment analysis.
- `requests` for API calls.
- `python-dotenv` to manage environment variables.


