# import streamlit as st
#
# import mysql.connector
#
# from mysql.connector import Error
#
# from llm_service import analyze_meeting_docx
#
# from email_service import send_meeting_email
#
# from reminder_service import set_task_reminders
#
# # -------------------- PAGE CONFIG --------------------
#
# st.set_page_config(
#
#     page_title="Smart Meeting Synthesizer | InnovateTech Solutions",
#
#     layout="wide",
#
#     page_icon="🤖"
#
# )
#
# # -------------------- CUSTOM CSS STYLING --------------------
#
# st.markdown("""
# <style>
#
#     /* General Layout */
#
#     body {
#
#         background: #f7f8fa;
#
#         color: #1c1c1c;
#
#         font-family: 'Segoe UI', Roboto, sans-serif;
#
#     }
#
#     .main-title {
#
#         text-align: center;
#
#         font-size: 40px;
#
#         font-weight: 700;
#
#         color: #2d3436;
#
#         margin-bottom: 10px;
#
#     }
#
#     .sub-text {
#
#         text-align: center;
#
#         color: #636e72;
#
#         font-size: 16px;
#
#         margin-bottom: 25px;
#
#     }
#
#     /* Divider */
#
#     .divider {
#
#         border: none;
#
#         height: 2px;
#
#         background: linear-gradient(to right, #0984e3, #6c5ce7);
#
#         margin: 10px 0 30px 0;
#
#     }
#
#     /* Buttons */
#
#     .stButton>button {
#
#         border-radius: 6px;
#
#         background-color: #0984e3;
#
#         color: #fff;
#
#         font-weight: 600;
#
#         transition: all 0.3s ease;
#
#         border: none;
#
#     }
#
#     .stButton>button:hover {
#
#         background-color: #74b9ff;
#
#         transform: scale(1.02);
#
#     }
#
#     /* Inputs */
#
#     .stTextInput>div>div>input {
#
#         border-radius: 6px;
#
#         border: 1px solid #dfe6e9;
#
#         padding: 8px;
#
#     }
#
#     /* Section Headers */
#
#     .section-header {
#
#         font-size: 24px;
#
#         color: #2d3436;
#
#         font-weight: 600;
#
#         margin-top: 20px;
#
#         margin-bottom: 10px;
#
#     }
#
#     /* Expander Styling */
#
#     .streamlit-expanderHeader {
#
#         font-weight: 600;
#
#         color: #2d3436;
#
#     }
#
#     /* Cards for sections */
#
#     .stCard {
#
#         background: #ffffff;
#
#         padding: 20px;
#
#         border-radius: 12px;
#
#         box-shadow: 0 2px 8px rgba(0,0,0,0.05);
#
#         margin-bottom: 25px;
#
#     }
# </style>
#
# """, unsafe_allow_html=True)
#
# # -------------------- SESSION STATE --------------------
#
# for key in ["logged_in", "user_email", "user_team", "summary"]:
#
#     if key not in st.session_state:
#         st.session_state[key] = "" if key != "logged_in" else False
#
#
# # -------------------- DATABASE CONNECTION --------------------
#
# def get_db_connection():
#     try:
#
#         conn = mysql.connector.connect(
#
#             host="localhost",
#
#             user="root",
#
#             password="1234",
#
#             database="meeting_ai"
#
#         )
#
#         return conn
#
#     except Error as e:
#
#         st.error(f"Database connection failed: {e}")
#
#         return None
#
#
# # -------------------- PAGE TITLE --------------------
#
# st.markdown("<h1 class='main-title'>Smart Meeting Synthesizer</h1>", unsafe_allow_html=True)
#
# st.markdown("<p class='sub-text'>Enhancing productivity through intelligent meeting insights</p>",
#             unsafe_allow_html=True)
#
# st.markdown("<hr class='divider'>", unsafe_allow_html=True)
#
# # -------------------- LOGIN SECTION --------------------
#
# if not st.session_state.logged_in:
#
#     with st.container():
#
#         st.markdown("<div class='stCard'>", unsafe_allow_html=True)
#
#         st.subheader("🔐 Employee Login")
#
#         st.markdown("Please log in using your registered **email** and **team name**.")
#
#         col1, col2 = st.columns(2)
#
#         with col1:
#
#             email = st.text_input("Email Address")
#
#         with col2:
#
#             team_name = st.text_input("Team Name")
#
#         if st.button("Login"):
#
#             conn = get_db_connection()
#
#             if conn:
#
#                 cursor = conn.cursor(dictionary=True)
#
#                 cursor.execute("SELECT * FROM users WHERE email = %s AND team_name = %s", (email, team_name))
#
#                 user = cursor.fetchone()
#
#                 cursor.close()
#
#                 conn.close()
#
#                 if user:
#
#                     st.session_state.logged_in = True
#
#                     st.session_state.user_email = email
#
#                     st.session_state.user_team = team_name
#
#                     st.success(f"Welcome back, {email}.")
#
#                     st.rerun()
#
#                 else:
#
#                     st.error("Invalid credentials. Please try again.")
#
#             else:
#
#                 st.error("Unable to connect to the company database.")
#
#         st.markdown("</div>", unsafe_allow_html=True)
#
# # -------------------- DASHBOARD --------------------
#
# else:
#
#     st.info(f"👋 Logged in as **{st.session_state.user_email}** | Team: **{st.session_state.user_team}**")
#
#     st.markdown("<hr class='divider'>", unsafe_allow_html=True)
#
#     # --- Fetch Team Members ---
#
#     conn = get_db_connection()
#
#     team_members = []
#
#     if conn:
#         cursor = conn.cursor(dictionary=True)
#
#         cursor.execute("SELECT email FROM users WHERE team_name = %s", (st.session_state.user_team,))
#
#         team_members = [row["email"] for row in cursor.fetchall()]
#
#         cursor.close()
#
#         conn.close()
#
#     # --- Upload Transcript ---
#
#     # st.markdown("<div class='stCard'>", unsafe_allow_html=True)
#     #
#     # st.markdown("<h2 class='section-header'>📄 Upload Meeting Transcript</h2>", unsafe_allow_html=True)
#     #
#     # uploaded_file = st.file_uploader("Upload your meeting transcript (.docx)", type=["docx"])
#     #
#     # if st.button("Analyze Transcript"):
#     #
#     #     if uploaded_file:
#     #
#     #         with st.spinner("Analyzing your meeting transcript..."):
#     #
#     #             try:
#     #
#     #                 result = analyze_meeting_docx(uploaded_file)
#     #
#     #                 if result.get("status") == "success":
#     #
#     #                     st.session_state.summary = result.get("content", "")
#     #
#     #                     st.success("Meeting successfully analyzed.")
#     #
#     #                     st.write(st.session_state.summary)
#     #
#     #                 else:
#     #
#     #                     st.error(result.get("message", "Error during analysis."))
#     #
#     #             except Exception as e:
#     #
#     #                 st.error(f"Analysis failed: {e}")
#     #
#     #     else:
#     #
#     #         st.warning("Please upload a .docx file before analyzing.")
#     #
#     # st.markdown("</div>", unsafe_allow_html=True)
#     from llm_service import analyze_meeting_docx, enhance_email_body
#
#     # --- Upload Transcript ---
#     st.markdown("<div class='stCard'>", unsafe_allow_html=True)
#     st.markdown("<h2 class='section-header'>📄 Upload Meeting Transcript</h2>", unsafe_allow_html=True)
#
#     uploaded_file = st.file_uploader("Upload your meeting transcript (.docx)", type=["docx"])
#
#     if st.button("Analyze Transcript"):
#         if uploaded_file:
#             with st.spinner("Analyzing your meeting transcript..."):
#                 try:
#                     result = analyze_meeting_docx(uploaded_file)
#
#                     if result.get("status") == "success":
#                         st.session_state.summary = result.get("content", "")
#                         st.success("✅ Meeting successfully analyzed.")
#
#                         # --- Auto enhance the summary for email format ---
#                         with st.spinner("✨ Preparing professional email draft..."):
#                             enhanced_email = enhance_email_body(st.session_state.summary)
#                             st.session_state.enhanced_email = enhanced_email
#
#                         # --- Display structured summary ---
#                         st.markdown("<h3 style='color:#2d3436;'>🧾 Structured Meeting Summary</h3>",
#                                     unsafe_allow_html=True)
#                         st.markdown(st.session_state.summary)
#
#                         # --- Display auto-enhanced email preview ---
#                         st.markdown("<hr class='divider'>", unsafe_allow_html=True)
#                         st.markdown("<h3 style='color:#2d3436;'>📧 Auto-Generated Email Format</h3>",
#                                     unsafe_allow_html=True)
#                         st.info("This is the final email body prepared automatically by the AI assistant.")
#                         st.markdown(f"""
#                         <div style='background-color:#f9fafb; padding:20px; border-radius:10px; line-height:1.6;'>
#                         {st.session_state.enhanced_email}
#                         </div>
#                         """, unsafe_allow_html=True)
#
#                     else:
#                         st.error(result.get("message", "Error during analysis."))
#
#                 except Exception as e:
#                     st.error(f"Analysis failed: {e}")
#         else:
#             st.warning("Please upload a .docx file before analyzing.")
#
#     st.markdown("</div>", unsafe_allow_html=True)
#
#     # --- Send Emails ---
#
#     if team_members and st.session_state.summary:
#
#         st.markdown("<div class='stCard'>", unsafe_allow_html=True)
#
#         st.markdown("<h2 class='section-header'>📧 Distribute Summary via Email</h2>", unsafe_allow_html=True)
#
#         recipients = st.multiselect("Select Recipients", team_members, default=team_members)
#
#         email_body = st.text_area("Email Content", st.session_state.summary, height=380)
#
#         if st.button("Send Meeting Summary"):
#
#             with st.spinner("Sending meeting summary emails..."):
#
#                 try:
#
#                     response = send_meeting_email(
#
#                         sender_email=st.session_state.user_email,
#
#                         recipients=recipients,
#
#                         subject="Meeting Summary",
#
#                         body=email_body
#
#                     )
#
#                     if response.get("status") == "success":
#
#                         st.success("Emails sent successfully.")
#
#                     else:
#
#                         st.error(response.get("message", "Email sending failed."))
#
#                 except Exception as e:
#
#                     st.error(f"Email dispatch failed: {e}")
#
#         st.markdown("</div>", unsafe_allow_html=True)
#
#     # --- Add Reminders ---
#
#     if st.session_state.summary:
#
#         st.markdown("<div class='stCard'>", unsafe_allow_html=True)
#
#         st.markdown("<h2 class='section-header'>⏰ Add Follow-up Reminders</h2>", unsafe_allow_html=True)
#
#         if st.button("Add Reminders to Calendar"):
#
#             with st.spinner("Syncing reminders to team calendar..."):
#
#                 try:
#
#                     set_task_reminders(st.session_state.summary)
#
#                     st.success("Reminders added successfully to your team calendar.")
#
#                 except Exception as e:
#
#                     st.error(f"Failed to add reminders: {e}")
#
#         st.markdown("</div>", unsafe_allow_html=True)
#
#     # --- Logout ---
#
#     st.markdown("<hr class='divider'>", unsafe_allow_html=True)
#
#     if st.button("Logout"):
#         st.session_state.logged_in = False
#
#         st.session_state.user_email = ""
#
#         st.session_state.user_team = ""
#
#         st.session_state.summary = ""
#
#         st.success("You have been logged out successfully.")
#
#         st.rerun()



############################# 2 not goood##########
# import streamlit as st
# import mysql.connector
# from mysql.connector import Error
#
# # -------------------- CONFIG --------------------
# st.set_page_config(page_title="🤖 Smart Meeting Synthesizer", layout="wide")
#
# # -------------------- UI STYLE (SmartBench design) --------------------
# def load_css():
#     st.markdown("""
#     <style>
#         body { background: linear-gradient(135deg, #1f1f2e, #3b3b98, #6a89cc); color: white; font-family: 'Segoe UI'; }
#         .stButton>button { border-radius: 10px; background-color: #6c63ff; color: white; font-weight: bold; transition: 0.3s; }
#         .stButton>button:hover { background-color: #a29bfe; transform: scale(1.05); }
#         .stTextInput>div>div>input { border-radius: 8px; }
#         .main-title { text-align: center; font-size: 42px; font-weight: bold; color: #ffffff; margin-top: -30px; text-shadow: 2px 2px 10px #000; }
#         .section-header { font-size: 26px; color: #ffeaa7; margin-top: 20px; }
#         .divider { border: none; height: 2px; background: linear-gradient(to right, #00cec9, #6c5ce7, #fd79a8); margin: 15px 0; }
#     </style>
#     """, unsafe_allow_html=True)
#
# # -------------------- CORE LAYER --------------------
# def get_db_connection():
#     """Database connection (Model layer)"""
#     try:
#         return mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="1234",
#             database="meeting_ai"
#         )
#     except Error as e:
#         st.error(f"❌ Database connection error: {e}")
#         return None
#
#
# def authenticate_user(email, team_name):
#     """Authentication logic"""
#     conn = get_db_connection()
#     if not conn:
#         return False, "⚠️ Could not connect to database."
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM users WHERE email=%s AND team_name=%s", (email, team_name))
#     user = cursor.fetchone()
#     cursor.close()
#     conn.close()
#     if user:
#         st.session_state.logged_in = True
#         st.session_state.user_email = email
#         st.session_state.user_team = team_name
#         return True, f"✅ Welcome, {email}!"
#     else:
#         return False, "❌ Invalid credentials."
#
#
# def fetch_team_members(team_name):
#     """Fetch all team members"""
#     conn = get_db_connection()
#     if not conn:
#         return []
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT email FROM users WHERE team_name=%s", (team_name,))
#     members = [row["email"] for row in cursor.fetchall()]
#     cursor.close()
#     conn.close()
#     return members
#
# # -------------------- SERVICE LAYER (Mocked) --------------------
# def analyze_meeting_docx(file):
#     """LLM-based meeting analysis"""
#     # Placeholder: Replace with real model call
#     return {"status": "success", "content": "Key Discussion Points:\n1. Launch timeline agreed for next week.\n2. Marketing team to finalize campaign.\n3. Tech team to update deployment pipeline."}
#
#
# def send_meeting_email(sender_email, recipients, subject, body):
#     """Email sender mock"""
#     if not recipients or not body:
#         return {"status": "error", "message": "Missing recipients or email content"}
#     return {"status": "success", "message": f"Emails sent to {', '.join(recipients)}"}
#
#
# def set_task_reminders(summary_text):
#     """Mock reminder creation"""
#     return {"status": "success", "message": "Reminders successfully added."}
#
#
# # -------------------- UI COMPONENTS --------------------
# def show_login_section():
#     st.subheader("🔐 Login to Continue")
#     st.markdown("Enter your **email** and **team name** to access meeting tools.")
#     col1, col2 = st.columns(2)
#     email = col1.text_input("📧 Email")
#     team = col2.text_input("👥 Team Name")
#     if st.button("Login"):
#         success, msg = authenticate_user(email, team)
#         if success:
#             st.success(msg)
#             st.balloons()
#             st.rerun()
#         else:
#             st.error(msg)
#
#
# def show_dashboard():
#     """Main dashboard after login"""
#     st.success(f"👋 Logged in as **{st.session_state.user_email}** | Team: **{st.session_state.user_team}**")
#     st.markdown("<hr class='divider'>", unsafe_allow_html=True)
#
#     # --- TEAM MEMBERS ---
#     members = fetch_team_members(st.session_state.user_team)
#
#     # --- Upload Transcript ---
#     st.markdown("<h2 class='section-header'>📄 Upload Meeting Transcript</h2>", unsafe_allow_html=True)
#     with st.expander("Click to upload and analyze your meeting transcript"):
#         uploaded_file = st.file_uploader("Choose a .docx file", type=["docx"])
#         if st.button("🔍 Analyze Transcript") and uploaded_file:
#             with st.spinner("🧠 Analyzing transcript..."):
#                 result = analyze_meeting_docx(uploaded_file)
#                 if result["status"] == "success":
#                     st.session_state.summary = result["content"]
#                     st.success("✅ Analysis complete!")
#                     st.text_area("📝 Meeting Summary", st.session_state.summary, height=200)
#                 else:
#                     st.error(result.get("message", "Analysis failed"))
#
#     # --- Send Emails ---
#     if members:
#         st.markdown("<h2 class='section-header'>📧 Send Meeting Summary</h2>", unsafe_allow_html=True)
#         with st.expander("Click to view email options"):
#             recipients = st.multiselect("Select Recipients", members, default=members)
#             email_body = st.text_area("Email Content", st.session_state.get("summary", ""), height=150)
#             if st.button("📨 Send Email"):
#                 with st.spinner("✉️ Sending emails..."):
#                     res = send_meeting_email(st.session_state.user_email, recipients, "Meeting Summary", email_body)
#                     if res["status"] == "success":
#                         st.success(res["message"])
#                         st.snow()
#                     else:
#                         st.error(res["message"])
#     else:
#         st.warning("⚠️ No team members found in your team.")
#
#     # --- Add Reminders ---
#     if st.session_state.get("summary"):
#         st.markdown("<h2 class='section-header'>⏰ Add Reminders</h2>", unsafe_allow_html=True)
#         with st.expander("Click to add reminders to shared calendar"):
#             if st.button("🗓️ Add Reminders"):
#                 with st.spinner("Adding reminders..."):
#                     res = set_task_reminders(st.session_state.summary)
#                     if res["status"] == "success":
#                         st.success(res["message"])
#                         st.balloons()
#                     else:
#                         st.error(res["message"])
#
#     # --- Logout ---
#     st.markdown("<hr class='divider'>", unsafe_allow_html=True)
#     if st.button("🚪 Logout"):
#         for k in list(st.session_state.keys()):
#             del st.session_state[k]
#         st.success("👋 Logged out successfully!")
#         st.rerun()
#
#
# # -------------------- MAIN CONTROLLER --------------------
# def main():
#     load_css()
#
#     # Initialize session vars
#     for key, val in {
#         "logged_in": False,
#         "user_email": "",
#         "user_team": "",
#         "summary": ""
#     }.items():
#         if key not in st.session_state:
#             st.session_state[key] = val
#
#     # Title
#     st.markdown("<h1 class='main-title'>🚀 Smart Meeting Synthesizer</h1>", unsafe_allow_html=True)
#     st.markdown("<hr class='divider'>", unsafe_allow_html=True)
#
#     if not st.session_state.logged_in:
#         show_login_section()
#     else:
#         show_dashboard()
#
#
# # -------------------- RUN APP --------------------
# if __name__ == "__main__":
#     main()
#



import streamlit as st
import mysql.connector
from mysql.connector import Error
from llm_service import analyze_meeting_docx, enhance_email_body
from email_service import send_meeting_email
from reminder_service import set_task_reminders

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Smart Meeting Synthesizer | InnovateTech Solutions",
    layout="wide",
    page_icon="🤖"
)

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
    body {
        background: #f4f6fa;
        color: #2c3e50;
        font-family: 'Segoe UI', Roboto, sans-serif;
    }

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        color: #1e3799;
        margin-bottom: 8px;
    }

    .sub-text {
        text-align: center;
        color: #636e72;
        font-size: 17px;
        margin-bottom: 30px;
    }

    .divider {
        border: none;
        height: 2px;
        background: linear-gradient(to right, #0984e3, #6c5ce7);
        margin: 10px 0 30px 0;
    }

    .stButton>button {
        border-radius: 8px;
        background: linear-gradient(90deg, #0984e3, #6c5ce7);
        color: white;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
    }

    .stButton>button:hover {
        transform: scale(1.03);
        background: linear-gradient(90deg, #6c5ce7, #0984e3);
    }

    .stCard {
        background: white;
        padding: 25px;
        border-radius: 14px;
        box-shadow: 0px 3px 12px rgba(0,0,0,0.08);
        margin-bottom: 25px;
    }

    .section-header {
        font-size: 24px;
        color: #2d3436;
        font-weight: 600;
        margin-bottom: 15px;
    }

    .recipient-checkbox {
        margin: 8px 0;
    }

</style>
""", unsafe_allow_html=True)

# -------------------- SESSION STATE --------------------
for key in ["logged_in", "user_email", "user_team", "summary", "enhanced_email"]:
    if key not in st.session_state:
        st.session_state[key] = "" if key != "logged_in" else False

# -------------------- SIDEBAR --------------------
st.sidebar.title("🧭 Smart Meeting Guide")
st.sidebar.markdown("""
### About
Smart Meeting Synthesizer automatically extracts insights, actions, and decisions from your meeting transcript.

### Steps:
1️⃣ Upload meeting transcript (.docx)  
2️⃣ View AI-generated summary  
3️⃣ Automatically generate a professional email  
4️⃣ Edit email and send to team  
5️⃣ Optionally set reminders  

✨ **Powered by InnovateTech AI**
""")

# -------------------- DB CONNECTION --------------------
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="meeting_ai"
        )
        return conn
    except Error as e:
        st.error(f"Database connection failed: {e}")
        return None

# -------------------- TITLE --------------------
st.markdown("<h1 class='main-title'>Smart Meeting Synthesizer</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>Transform your meetings into actionable intelligence.</p>", unsafe_allow_html=True)
st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# -------------------- LOGIN --------------------
if not st.session_state.logged_in:
    st.markdown("<div class='stCard'>", unsafe_allow_html=True)
    st.subheader("🔐 Employee Login")
    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input("Email Address").strip().lower()
    with col2:
        team_name = st.text_input("Team Name").strip().lower()

    if st.button("Login"):
        try:
            conn = get_db_connection()
            if not conn:
                st.error("❌ Database connection failed.")
            else:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(
                    "SELECT * FROM users WHERE LOWER(email) = %s AND LOWER(team_name) = %s",
                    (email, team_name)
                )
                user = cursor.fetchone()
                cursor.close()
                conn.close()

                if user:
                    st.session_state.logged_in = True
                    st.session_state.user_email = user["email"]
                    st.session_state.user_team = user["team_name"]
                    st.success(f"✅ Welcome, {st.session_state.user_email}")
                    st.rerun()
                else:
                    st.error("Invalid credentials. Check your email or team name.")
        except Exception as e:
            st.error(f"⚠️ Login failed due to: {e}")
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- DASHBOARD --------------------
else:
    st.info(f"👋 Logged in as **{st.session_state.user_email}** | Team: **{st.session_state.user_team}**")
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # --- Fetch Team Members ---
    conn = get_db_connection()
    team_members = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT email FROM users WHERE team_name = %s", (st.session_state.user_team,))
        team_members = [row["email"] for row in cursor.fetchall()]
        cursor.close()
        conn.close()

    # --- Upload Transcript ---
    st.markdown("<div class='stCard'>", unsafe_allow_html=True)
    st.markdown("<h2 class='section-header'>📄 Upload Meeting Transcript</h2>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload your meeting transcript (.docx)", type=["docx"])

    if st.button("Analyze Transcript"):
        if uploaded_file:
            with st.spinner("🔍 Analyzing your meeting transcript..."):
                try:
                    result = analyze_meeting_docx(uploaded_file)
                    if result.get("status") == "success":
                        st.session_state.summary = result.get("content", "")
                        st.success("✅ Meeting summary generated successfully.")

                        st.markdown("<h3 class='section-header'>🧾 Meeting Summary</h3>", unsafe_allow_html=True)
                        st.write(st.session_state.summary)

                        # Auto-enhance email after summary
                        with st.spinner("✨ Generating professional email draft..."):
                            enhanced = enhance_email_body(st.session_state.summary)
                            st.session_state.enhanced_email = enhanced or st.session_state.summary

                        st.markdown("<h3 class='section-header'>📧 Enhanced Email Draft</h3>", unsafe_allow_html=True)
                        st.session_state.enhanced_email = st.text_area(
                            "Edit Email Draft",
                            st.session_state.enhanced_email,
                            height=250
                        )
                    else:
                        st.error(result.get("message", "Error during analysis."))
                except Exception as e:
                    st.error(f"Analysis failed: {e}")
        else:
            st.warning("Please upload a .docx file before analyzing.")
    st.markdown("</div>", unsafe_allow_html=True)

    # --- Email Sending Section ---
    if team_members and st.session_state.enhanced_email:
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.markdown("<h2 class='section-header'>✉️ Send Meeting Summary</h2>", unsafe_allow_html=True)

        st.write("Select recipients to send this email:")
        selected_recipients = []
        for member in team_members:
            if st.checkbox(member, key=f"chk_{member}"):
                selected_recipients.append(member)

        if selected_recipients:
            st.write("**Selected Recipients:**")
            st.markdown(", ".join(selected_recipients))

        if st.button("📤 Send Meeting Summary"):
            if not selected_recipients:
                st.warning("Please select at least one recipient.")
            else:
                with st.spinner("Sending summary emails..."):
                    try:
                        response = send_meeting_email(
                            sender_email=st.session_state.user_email,
                            recipients=selected_recipients,
                            subject="Meeting Summary",
                            body=st.session_state.enhanced_email
                        )
                        if response.get("status") == "success":
                            st.success("✅ Emails sent successfully.")
                        else:
                            st.error(response.get("message", "Email sending failed."))
                    except Exception as e:
                        st.error(f"Email dispatch failed: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- Reminders Section ---
    if st.session_state.summary:
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.markdown("<h2 class='section-header'>⏰ Add Follow-up Reminders</h2>", unsafe_allow_html=True)
        if st.button("Add Reminders to Calendar"):
            with st.spinner("Syncing reminders..."):
                try:
                    set_task_reminders(st.session_state.summary)
                    st.success("Reminders added successfully.")
                except Exception as e:
                    st.error(f"Failed to add reminders: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- Logout ---
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    if st.button("Logout"):
        st.session_state.clear()
        st.success("You have been logged out successfully.")
        st.rerun()

