import streamlit as st
import requests

# FastAPI backend URL
BACKEND_URL = "http://127.0.0.1:8000/process_query"

st.set_page_config(page_title="LangGraph AI Assistant", layout="centered")

# Page title
st.title("LangGraph AI Assistant")
st.write("Enter your query below — the system will parse and execute it intelligently.")

# Text input
user_query = st.text_input("Your Query:", placeholder="e.g., add 5 and 10 or What is today's date?")

# Submit button
if st.button("Submit"):
    if not user_query.strip():
        st.warning("Please enter a query before submitting.")
    else:
        with st.spinner("Processing your query..."):
            try:
                response = requests.post(
                    BACKEND_URL,
                    json={"query": user_query},
                    timeout=15
                )

                if response.status_code == 200:
                    data = response.json()
                    st.success("✅ Result:")
                    st.write(data.get("result", "No result found."))
                else:
                    st.error(f"❌ Server error: {response.status_code}")
                    st.text(response.text)

            except requests.exceptions.RequestException as e:
                st.error("⚠️ Could not connect to backend.")
                st.text(str(e))
