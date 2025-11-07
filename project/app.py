# import streamlit as st
# from dotenv import load_dotenv
# import os
# from langgraph_workflow import workflow  # This is already a compiled graph
#
# # Load environment variables from .env file
# load_dotenv()
#
# # Get API keys from environment variables
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
#
# # Set up Streamlit app
# st.title("Stock Insights with LangGraph and AI")
#
# # User input for query
# user_query = st.text_input("Enter your stock query (e.g., 'What are the insights about Tata Motors?')")
#
# # Button to process query
# if st.button("Get Insights"):
#     if user_query:
#         # Run the workflow with the user query
#         result = workflow.invoke({"user_query": user_query})
#
#         # Display results
#         st.write(f"### Current Stock Price for {result['stock_symbol']}: ₹{result['stock_data'][-1]['Close']}")
#         st.write(f"### 7-Day Stock Data:")
#         st.dataframe(result['stock_data'])
#         st.write(f"### News Summary:")
#         st.write(result['news_summary'])
#         st.write(f"### AI Insights:")
#         st.write(result['insights'])


# import streamlit as st
# from dotenv import load_dotenv
# import os
# from langgraph_workflow import workflow  # This is already a compiled graph
#
# # Load environment variables
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
#
# # Initialize session state for chat history
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
#
# # Streamlit app title
# st.title("Stock Insights Chatbot with LangGraph and AI")
#
# # User input
# user_query = st.text_input("Enter your stock query (e.g., 'Insights about Tata Motors?')")
#
# # Button to submit query
# if st.button("Send"):
#     if user_query:
#         # Invoke workflow for current query
#         result = workflow.invoke({"user_query": user_query})
#
#         # Prepare response
#         response = {
#             "query": user_query,
#             "stock_symbol": result.get("stock_symbol", "N/A"),
#             "stock_data": result.get("stock_data", []),
#             "news_summary": result.get("news_summary", ""),
#             "insights": result.get("insights", "")
#         }
#
#         # Append to chat history
#         st.session_state.chat_history.append(response)
#
# # Display chat history like a conversation
# for chat in reversed(st.session_state.chat_history):
#     st.markdown(f"**You:** {chat['query']}")
#     if chat['stock_data']:
#         st.markdown(f"**Current Stock Price for {chat['stock_symbol']}:** ₹{chat['stock_data'][-1]['Close']}")
#         st.markdown("**7-Day Stock Data:**")
#         st.dataframe(chat['stock_data'])
#     if chat['news_summary']:
#         st.markdown("**News Summary:**")
#         st.write(chat['news_summary'])
#     if chat['insights']:
#         st.markdown("**AI Insights:**")
#         st.write(chat['insights'])
#     st.markdown("---")



# import streamlit as st
# from dotenv import load_dotenv
# import os
# from langgraph_workflow import workflow  # Your compiled LangGraph workflow
#
# # Load environment variables
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
#
# # Initialize session state for chat history
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
#
# st.title("📊 Stock Insights Chatbot with Sentiment Analysis")
#
# # User input with placeholder
# user_query = st.text_input(
#     "Enter your stock query (e.g., 'Insights about Tata Motors?')",
#     placeholder="Type your question here..."
# )
#
# # Process button with loading spinner
# if st.button("🤖 Get Insights"):
#     if user_query.strip():
#         with st.spinner("Processing your request..."):
#             try:
#                 result = workflow.invoke({"user_query": user_query})
#                 response = {
#                     "query": user_query,
#                     "stock_symbol": result.get("stock_symbol", "N/A"),
#                     "stock_data": result.get("stock_data", []),
#                     "news_summary": result.get("news_summary", ""),
#                     "sentiment_analyzed_articles": result.get("sentiment_analyzed_articles", []),
#                     "insights": result.get("insights", "")
#                 }
#                 st.session_state.chat_history.append(response)
#             except Exception as e:
#                 st.error(f"Oops! Something went wrong: {e}")
#     else:
#         st.warning("Please enter a valid query.")
#
# # Display chat history as conversation
# for chat in reversed(st.session_state.chat_history):
#     st.markdown(f"You: {chat['query']}")
#
#     if chat['stock_data']:
#         st.markdown(f"### Stock Price for {chat['stock_symbol']}")
#         latest_close = chat['stock_data'][-1]['Close']
#         st.markdown(f"**Latest Close Price:** ₹{latest_close}")
#         st.dataframe(chat['stock_data'])
#
#     if chat['news_summary']:
#         st.markdown("### News Summary")
#         st.write(chat['news_summary'])
#
#     if chat['sentiment_analyzed_articles']:
#         st.markdown("### Sentiment Analysis of Recent News Articles")
#         for article in chat['sentiment_analyzed_articles'][:5]:
#             st.markdown(f"- **{article.get('title', 'No Title')}**")
#             sentiment = article.get('sentiment', {})
#             label = sentiment.get('label', 'neutral')
#             score = sentiment.get('score', 0)
#             st.markdown(f"  Sentiment: **{label.capitalize()}** (Confidence: {score:.2f})")
#             st.markdown(f"  [Read more]({article.get('url', '#')})")
#
#     if chat['insights']:
#         st.markdown("### AI Insights")
#         st.write(chat['insights'])
#
#     st.markdown("---")

import streamlit as st
from dotenv import load_dotenv
import os
from langgraph_workflow import workflow  # Your compiled LangGraph workflow
import pandas as pd

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Info message in left corner - using st.sidebar for consistent positioning
st.sidebar.info(
    """
    ⚠️ This application is for analysis purposes only. It uses AI to generate insights. 
    Please make stock decisions sensibly
    """


)
st.sidebar.markdown(
    """
    ---
    Made using:  
    - Yahoo Finance (yfinance)  
    - FinBERT (Hugging Face)  
    - NewsAPI  
    - Gemini LLM
    """
)


st.title("📊 DeepStock AI : Intelligent Assistant for Stock Insights and finanacial Analysis")

# User input with placeholder
user_query = st.text_input(
    "Enter your stock query (e.g., 'Insights about Tata Motors?')",
    placeholder="Type your question here..."
)

# Process button with loading spinner
if st.button("🤖 Get Insights"):
    if user_query.strip():
        with st.spinner("Processing your request..."):
            try:
                result = workflow.invoke({"user_query": user_query})
                response = {
                    "query": user_query,
                    "stock_symbol": result.get("stock_symbol", "N/A"),
                    "stock_data": result.get("stock_data", []),
                    "news_summary": result.get("news_summary", ""),
                    "sentiment_analyzed_articles": result.get("sentiment_analyzed_articles", []),
                    "insights": result.get("insights", "")
                }
                st.session_state.chat_history.append(response)
            except Exception as e:
                st.error(f"Oops! Something went wrong: {e}")
    else:
        st.warning("Please enter a valid query.")

# Display chat history as conversation
for chat in reversed(st.session_state.chat_history):
    st.markdown(f"You: {chat['query']}")
    st.markdown("---")

    if chat['stock_data']:
        st.markdown(f"### Stock Price for {chat['stock_symbol']}")
        latest_close = chat['stock_data'][-1]['Close']
        st.markdown(f"**Latest Close Price:** ₹{latest_close}")
        st.markdown("---")
        st.markdown(f"### Stock Price for {chat['stock_symbol']}")
        latest_close = chat['stock_data'][-1]['Close']
        st.markdown(f"**Latest Close Price:** ₹{latest_close}")
        st.markdown("---")

        # Convert stock_data list of dicts to DataFrame
        df_stock = pd.DataFrame(chat['stock_data'])

        # Create numeric index from 0 to n-1 if no date/index column
        df_stock.index = range(len(df_stock))
        df_stock.index.name = "Day"  # Optional: name the index for clarity

        # Plot line chart of Close prices using numeric index
        st.line_chart(df_stock['Close'])
        st.markdown("---")

        st.dataframe(df_stock)

    if chat['news_summary']:
        st.markdown("### News Summary")
        st.write(chat['news_summary'])
        st.markdown("---")

    if chat['sentiment_analyzed_articles']:
        st.markdown("### Sentiment Analysis of Recent News Articles")
        # Display each article as a tile with sentiment summary
        for article in chat['sentiment_analyzed_articles'][:5]:
            title = article.get('title', 'No Title')
            sentiment = article.get('sentiment', {})
            label = sentiment.get('label', 'neutral').capitalize()
            score = sentiment.get('score', 0)
            url = article.get('url', '#')

            # Use st.markdown with some formatting for the tile effect
            st.markdown(
                f"""
                <div style="border:1px solid #ddd; padding:10px; margin-bottom:10px; border-radius:5px;">
                    <h4 style="margin: 0 0 5px 0;">{title}</h4>
                    <p style="margin:0 0 5px 0;">Sentiment: <b>{label}</b> (Confidence: {score:.2f})</p>
                    <a href="{url}" target="_blank" rel="noopener">Read more</a>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.markdown("---")

    if chat['insights']:
        st.markdown("### AI Insights")
        st.write(chat['insights'])
        st.markdown("---")


