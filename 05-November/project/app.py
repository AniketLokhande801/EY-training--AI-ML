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


import streamlit as st
from dotenv import load_dotenv
import os
from langgraph_workflow import workflow  # This is already a compiled graph

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Streamlit app title
st.title("Stock Insights Chatbot with LangGraph and AI")

# User input
user_query = st.text_input("Enter your stock query (e.g., 'Insights about Tata Motors?')")

# Button to submit query
if st.button("Send"):
    if user_query:
        # Invoke workflow for current query
        result = workflow.invoke({"user_query": user_query})

        # Prepare response
        response = {
            "query": user_query,
            "stock_symbol": result.get("stock_symbol", "N/A"),
            "stock_data": result.get("stock_data", []),
            "news_summary": result.get("news_summary", ""),
            "insights": result.get("insights", "")
        }

        # Append to chat history
        st.session_state.chat_history.append(response)

# Display chat history like a conversation
for chat in reversed(st.session_state.chat_history):
    st.markdown(f"**You:** {chat['query']}")
    if chat['stock_data']:
        st.markdown(f"**Current Stock Price for {chat['stock_symbol']}:** ₹{chat['stock_data'][-1]['Close']}")
        st.markdown("**7-Day Stock Data:**")
        st.dataframe(chat['stock_data'])
    if chat['news_summary']:
        st.markdown("**News Summary:**")
        st.write(chat['news_summary'])
    if chat['insights']:
        st.markdown("**AI Insights:**")
        st.write(chat['insights'])
    st.markdown("---")

