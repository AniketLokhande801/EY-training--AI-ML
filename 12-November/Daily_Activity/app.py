import streamlit as st
import requests
import json

# Backend endpoint
API_URL = "http://127.0.0.1:8000/analyze_meeting"

st.set_page_config(page_title="AI Meeting Insights", page_icon="🤖", layout="wide")

st.title("🤖 AI Meeting Insights Generator")
st.markdown("Upload a Microsoft Teams **.docx transcript** to automatically generate:")
st.markdown("- 📝 Concise Meeting Summary")
st.markdown("- 📄 Detailed Minutes of Meeting (MOM)")
st.markdown("- ✅ Action Items with Person & Deadline")

uploaded_file = st.file_uploader("Upload your meeting transcript (.docx)", type=["docx"])

if uploaded_file is not None:
    if st.button("Analyze Transcript"):
        with st.spinner("Analyzing meeting transcript..."):
            # Send file to FastAPI backend
            files = {"file": (uploaded_file.name, uploaded_file, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
            response = requests.post(API_URL, files=files)

            if response.status_code == 200:
                data = response.json()
                result = data.get("result", "")

                # Split by section headers for better display
                st.markdown("---")
                st.success("✅ **Analysis Completed!**")

                # Try to display structured sections
                sections = result.split("### ")
                for section in sections:
                    if not section.strip():
                        continue
                    header, *content = section.split("\n", 1)
                    st.subheader(header.strip())
                    st.markdown(content[0] if content else "")

            else:
                st.error(f"Error: {response.json().get('error', 'Unknown error')}")
