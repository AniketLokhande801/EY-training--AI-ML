import streamlit as st
import requests

st.set_page_config(page_title="Meeting Analyzer & Mailer", page_icon="📧")

st.title("📄 AI Meeting Transcript Analyzer + Email Sender")

# Upload transcript
uploaded_file = st.file_uploader("Upload meeting transcript (.docx)", type=["docx"])

# Step 1: Analyze Transcript
if uploaded_file and st.button("Analyze Transcript"):
    with st.spinner("Analyzing meeting transcript..."):
        files = {"file": uploaded_file.getvalue()}
        response = requests.post("http://127.0.0.1:8000/analyze_meeting/", files={"file": uploaded_file})

    if response.status_code == 200:
        res = response.json()
        if res["status"] == "success":
            st.session_state["analysis_result"] = res["content"]
            st.success("✅ Transcript analyzed successfully!")
            st.markdown(res["content"])
        else:
            st.error("❌ Analysis failed. Check backend logs.")
    else:
        st.error("⚠️ Something went wrong. Check your FastAPI backend.")

# Step 2: Email Section (after analysis)
if "analysis_result" in st.session_state:
    st.markdown("---")
    st.subheader("📨 Send Meeting Summary to Attendees")

    emails = st.text_area("Enter recipient emails (comma-separated):")
    if emails:
        if st.button("Send Emails"):
            with st.spinner("Sending email..."):
                data = {
                    "emails": emails,
                    "content": st.session_state["analysis_result"]
                }
                response = requests.post("http://127.0.0.1:8000/send_emails/", data=data)

            if response.status_code == 200:
                res = response.json()
                if res["status"] == "success":
                    st.success(f"✅ Email sent to: {', '.join(res['recipients'])}")
                else:
                    st.error("❌ Failed to send email.")
            else:
                st.error("⚠️ Backend error during email sending.")
