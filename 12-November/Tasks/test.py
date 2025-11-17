# import streamlit as st
# import mysql.connector
# from mysql.connector import Error
# from llm_service import analyze_meeting_docx
# from email_service import send_meeting_email
# #
# # # -------------------- DATABASE CONNECTION --------------------
# def get_db_connection():
#     try:
#         conn = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="1234",
#             database="meeting_ai"
#         )
#         return conn
#     except Error as e:
#         st.error(f"❌ Database connection error: {e}")
#         return None
# #
# # # -------------------- STREAMLIT APP --------------------
# st.set_page_config(page_title="🚀 AI Meeting Assistant", layout="wide")
# st.title("🤖 AI Meeting Assistant")
#
# # Initialize session state
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False
# if "user_email" not in st.session_state:
#     st.session_state.user_email = ""
# if "user_team" not in st.session_state:
#     st.session_state.user_team = ""
# if "summary" not in st.session_state:
#     st.session_state.summary = ""
#
# # -------------------- LOGIN SECTION --------------------
# if not st.session_state.logged_in:
#     st.subheader("Login")
#     email = st.text_input("Email")
#     team_name = st.text_input("Team Name")
#     login_clicked = st.button("Login")
#
#     if login_clicked:
#         conn = get_db_connection()
#         if conn:
#             cursor = conn.cursor(dictionary=True)
#             cursor.execute(
#                 "SELECT * FROM users WHERE email = %s AND team_name = %s",
#                 (email, team_name)
#             )
#             user = cursor.fetchone()
#             cursor.close()
#             conn.close()
#
#             if user:
#                 st.session_state.logged_in = True
#                 st.session_state.user_email = email
#                 st.session_state.user_team = team_name
#                 st.success(f"✅ Login successful! Welcome {email}")
#             else:
#                 st.error("❌ User not found or team mismatch")
#         else:
#             st.error("❌ Cannot connect to database")
#
# # -------------------- DASHBOARD SECTION --------------------
# if st.session_state.logged_in:
#     st.subheader(f"Welcome, {st.session_state.user_email} (Team: {st.session_state.user_team})")
#     st.markdown("---")
#
#     # Fetch team members
#     conn = get_db_connection()
#     team_members = []
#     if conn:
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute(
#             "SELECT email FROM users WHERE team_name = %s",
#             (st.session_state.user_team,)
#         )
#         team_members = [row["email"] for row in cursor.fetchall()]
#         cursor.close()
#         conn.close()
#
#     # Upload Transcript
#     st.header("📄 Upload Meeting Transcript")
#     uploaded_file = st.file_uploader("Choose a .docx file", type=["docx"])
#     if st.button("Analyze Transcript") and uploaded_file:
#         with st.spinner("Analyzing transcript..."):
#             try:
#                 analysis_result = analyze_meeting_docx(uploaded_file)
#                 if analysis_result.get("status") == "success":
#                     st.session_state.summary = analysis_result.get("content", "")
#                     st.success("✅ Analysis Complete!")
#                     st.text_area("Meeting Summary", st.session_state.summary, height=200)
#                 else:
#                     st.error(analysis_result.get("message", "Error during analysis"))
#             except Exception as e:
#                 st.error(f"❌ Analysis failed: {e}")
#
#     # Send Emails
#     if team_members:
#         st.header("📧 Send Meeting Summary via Email")
#         recipients = st.multiselect("Select Recipients", team_members, default=team_members)
#         email_body = st.text_area("Email Content", st.session_state.get("summary", ""), height=150)
#         if st.button("Send Email") and recipients:
#             with st.spinner("Sending emails..."):
#                 try:
#                     response = send_meeting_email(
#                         sender_email=st.session_state.user_email,
#                         recipients=recipients,
#                         subject="Meeting Summary",
#                         body=email_body
#                     )
#                     if response.get("status") == "success":
#                         st.success(response.get("message", "Emails sent successfully!"))
#                     else:
#                         st.error(response.get("message", "Error sending emails"))
#                 except Exception as e:
#                     st.error(f"❌ Failed to send emails: {e}")
#     else:
#         st.warning("⚠️ No team members found in your team.")
#
#     # Logout button
#     if st.button("Logout"):
#         st.session_state.logged_in = False
#         st.session_state.user_email = ""
#         st.session_state.user_team = ""
#         st.session_state.summary = ""
#         st.experimental_rerun = lambda: None  # removed rerun


# # Add this import at the top
# from reminder_service import set_task_reminders
#
# # -------------------- DASHBOARD SECTION --------------------
# if st.session_state.logged_in:
#     st.subheader(f"Welcome, {st.session_state.user_email} (Team: {st.session_state.user_team})")
#     st.markdown("---")
#
#     # Fetch team members
#     conn = get_db_connection()
#     team_members = []
#     if conn:
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute(
#             "SELECT email FROM users WHERE team_name = %s",
#             (st.session_state.user_team,)
#         )
#         team_members = [row["email"] for row in cursor.fetchall()]
#         cursor.close()
#         conn.close()
#
#     # Upload Transcript
#     st.header("📄 Upload Meeting Transcript")
#     uploaded_file = st.file_uploader("Choose a .docx file", type=["docx"])
#     analyze_clicked = st.button("Analyze Transcript")  # store in a variable
#
#     if analyze_clicked and uploaded_file:
#         with st.spinner("Analyzing transcript..."):
#             try:
#                 analysis_result = analyze_meeting_docx(uploaded_file)
#                 if analysis_result.get("status") == "success":
#                     st.session_state.summary = analysis_result.get("content", "")
#                     st.success("✅ Analysis Complete!")
#                     st.text_area("Meeting Summary", st.session_state.summary, height=200)
#
#                     # ------------------ Add Reminders Button ------------------
#                     if st.button("Set Reminders in Team Calendar"):
#                         with st.spinner("Setting reminders..."):
#                             try:
#                                 set_task_reminders(st.session_state.summary)
#                                 st.success("✅ Reminders added to Team Calendar!")
#                             except Exception as e:
#                                 st.error(f"❌ Failed to set reminders: {e}")
#                 else:
#                     st.error(analysis_result.get("message", "Error during analysis"))
#             except Exception as e:
#                 st.error(f"❌ Analysis failed: {e}")
#
#     # Send Emails
#     if team_members:
#         st.header("📧 Send Meeting Summary via Email")
#         recipients = st.multiselect("Select Recipients", team_members, default=team_members)
#         email_body = st.text_area("Email Content", st.session_state.get("summary", ""), height=150)
#         if st.button("Send Email") and recipients:
#             with st.spinner("Sending emails..."):
#                 try:
#                     response = send_meeting_email(
#                         sender_email=st.session_state.user_email,
#                         recipients=recipients,
#                         subject="Meeting Summary",
#                         body=email_body
#                     )
#                     if response.get("status") == "success":
#                         st.success(response.get("message", "Emails sent successfully!"))
#                     else:
#                         st.error(response.get("message", "Error sending emails"))
#                 except Exception as e:
#                     st.error(f"❌ Failed to send emails: {e}")
#     else:
#         st.warning("⚠️ No team members found in your team.")
#
#     # Logout button
#     if st.button("Logout"):
#         st.session_state.logged_in = False
#         st.session_state.user_email = ""
#         st.session_state.user_team = ""
#         st.session_state.summary = ""
#         st.experimental_rerun = lambda: None  # removed rerun


# import streamlit as st
# import mysql.connector
# from mysql.connector import Error
# from llm_service import analyze_meeting_docx
# from email_service import send_meeting_email
# from reminder_service import set_task_reminders  # your Google Calendar / Teams reminders service
#
# # -------------------- Initialize Session State --------------------
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False
# if "user_email" not in st.session_state:
#     st.session_state.user_email = ""
# if "user_team" not in st.session_state:
#     st.session_state.user_team = ""
# if "summary" not in st.session_state:
#     st.session_state.summary = ""
#
# # -------------------- DATABASE CONNECTION --------------------
# def get_db_connection():
#     try:
#         conn = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="1234",
#             database="meeting_ai"
#         )
#         return conn
#     except Error as e:
#         st.error(f"❌ Database connection error: {e}")
#         return None
#
# # -------------------- STREAMLIT APP --------------------
# st.set_page_config(page_title="🚀 AI Meeting Assistant", layout="wide")
# st.title("🤖 AI Meeting Assistant")
#
# # -------------------- LOGIN SECTION --------------------
# if not st.session_state.logged_in:
#     st.subheader("Login")
#     email = st.text_input("Email")
#     team_name = st.text_input("Team Name")
#     login_clicked = st.button("Login")
#
#     if login_clicked:
#         conn = get_db_connection()
#         if conn:
#             cursor = conn.cursor(dictionary=True)
#             cursor.execute(
#                 "SELECT * FROM users WHERE email = %s AND team_name = %s",
#                 (email, team_name)
#             )
#             user = cursor.fetchone()
#             cursor.close()
#             conn.close()
#
#             if user:
#                 st.session_state.logged_in = True
#                 st.session_state.user_email = email
#                 st.session_state.user_team = team_name
#                 st.success(f"✅ Login successful! Welcome {email}")
#             else:
#                 st.error("❌ User not found or team mismatch")
#         else:
#             st.error("❌ Cannot connect to database")
#
# # -------------------- DASHBOARD SECTION --------------------
# if st.session_state.logged_in:
#     st.subheader(f"Welcome, {st.session_state.user_email} (Team: {st.session_state.user_team})")
#     st.markdown("---")
#
#     # Fetch team members
#     conn = get_db_connection()
#     team_members = []
#     if conn:
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute(
#             "SELECT email FROM users WHERE team_name = %s",
#             (st.session_state.user_team,)
#         )
#         team_members = [row["email"] for row in cursor.fetchall()]
#         cursor.close()
#         conn.close()
#
#     # Upload Transcript
#     st.header("📄 Upload Meeting Transcript")
#     uploaded_file = st.file_uploader("Choose a .docx file", type=["docx"])
#     analyze_clicked = st.button("Analyze Transcript")
#
#     if analyze_clicked and uploaded_file:
#         with st.spinner("Analyzing transcript..."):
#             try:
#                 analysis_result = analyze_meeting_docx(uploaded_file)
#                 if analysis_result.get("status") == "success":
#                     st.session_state.summary = analysis_result.get("content", "")
#                     st.success("✅ Analysis Complete!")
#                     st.text_area("Meeting Summary", st.session_state.summary, height=200)
#                 else:
#                     st.error(analysis_result.get("message", "Error during analysis"))
#             except Exception as e:
#                 st.error(f"❌ Analysis failed: {e}")
#
#     # Send Emails
#     if team_members:
#         st.header("📧 Send Meeting Summary via Email")
#         recipients = st.multiselect("Select Recipients", team_members, default=team_members)
#         email_body = st.text_area("Email Content", st.session_state.get("summary", ""), height=150)
#         send_email_clicked = st.button("Send Email")
#
#         if send_email_clicked and recipients:
#             with st.spinner("Sending emails..."):
#                 try:
#                     response = send_meeting_email(
#                         sender_email=st.session_state.user_email,
#                         recipients=recipients,
#                         subject="Meeting Summary",
#                         body=email_body
#                     )
#                     if response.get("status") == "success":
#                         st.success(response.get("message", "Emails sent successfully!"))
#                     else:
#                         st.error(response.get("message", "Error sending emails"))
#                 except Exception as e:
#                     st.error(f"❌ Failed to send emails: {e}")
#     else:
#         st.warning("⚠️ No team members found in your team.")
#
#     # Add Reminders Button
#     if st.session_state.summary:
#         st.header("⏰ Add Reminders to Team Calendar")
#         add_reminders_clicked = st.button("Add Reminders")
#
#         if add_reminders_clicked:
#             with st.spinner("Adding reminders..."):
#                 try:
#                     set_task_reminders(st.session_state.summary)
#                     st.success("✅ Reminders added to the shared calendar!")
#                 except Exception as e:
#                     st.error(f"❌ Failed to add reminders: {e}")
#
#     # Logout button
#     if st.button("Logout"):
#         st.session_state.logged_in = False
#         st.session_state.user_email = ""
#         st.session_state.user_team = ""
#         st.session_state.summary = ""
#         st.experimental_rerun()

#
# import streamlit as st
# import mysql.connector
# from mysql.connector import Error
# from llm_service import analyze_meeting_docx
# from email_service import send_meeting_email
# from reminder_service import set_task_reminders
#
#
# # -------------------- PAGE CONFIG --------------------
# st.set_page_config(page_title="🤖 Smart Meeting Synthesizer", layout="wide")
#
# # -------------------- CUSTOM CSS STYLING --------------------
# st.markdown("""
# <style>
#     body {
#         background: linear-gradient(135deg, #1f1f2e, #3b3b98, #6a89cc);
#         color: white;
#         font-family: 'Segoe UI', sans-serif;
#     }
#     .stButton>button {
#         border-radius: 10px;
#         background-color: #6c63ff;
#         color: white;
#         font-weight: bold;
#         transition: 0.3s;
#     }
#     .stButton>button:hover {
#         background-color: #a29bfe;
#         transform: scale(1.05);
#     }
#     .stTextInput>div>div>input {
#         border-radius: 8px;
#     }
#     .main-title {
#         text-align: center;
#         font-size: 42px;
#         font-weight: bold;
#         color: #ffffff;
#         margin-top: -30px;
#         text-shadow: 2px 2px 10px #000000;
#     }
#     .section-header {
#         font-size: 26px;
#         color: #ffeaa7;
#         margin-top: 20px;
#     }
#     .divider {
#         border: none;
#         height: 2px;
#         background: linear-gradient(to right, #00cec9, #6c5ce7, #fd79a8);
#         margin-top: 15px;
#         margin-bottom: 20px;
#     }
# </style>
# """, unsafe_allow_html=True)
#
# # -------------------- INITIALIZE SESSION --------------------
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False
# if "user_email" not in st.session_state:
#     st.session_state.user_email = ""
# if "user_team" not in st.session_state:
#     st.session_state.user_team = ""
# if "summary" not in st.session_state:
#     st.session_state.summary = ""
#
#
# # -------------------- DATABASE CONNECTION --------------------
# def get_db_connection():
#     try:
#         conn = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="1234",
#             database="meeting_ai"
#         )
#         return conn
#     except Error as e:
#         st.error(f"❌ Database connection error: {e}")
#         return None
#
#
# # -------------------- TITLE --------------------
# st.markdown("<h1 class='main-title'>🚀 Smart Meeting Synthesizer</h1>", unsafe_allow_html=True)
# st.markdown("<hr class='divider'>", unsafe_allow_html=True)
#
# # -------------------- LOGIN SECTION --------------------
# if not st.session_state.logged_in:
#     with st.container():
#         st.subheader("🔐 Login to Continue")
#         st.markdown("Enter your **email** and **team name** to access meeting tools.")
#         col1, col2 = st.columns(2)
#         with col1:
#             email = st.text_input("📧 Email")
#         with col2:
#             team_name = st.text_input("👥 Team Name")
#
#         login_clicked = st.button("Login")
#
#         if login_clicked:
#             conn = get_db_connection()
#             if conn:
#                 cursor = conn.cursor(dictionary=True)
#                 cursor.execute("SELECT * FROM users WHERE email = %s AND team_name = %s", (email, team_name))
#                 user = cursor.fetchone()
#                 cursor.close()
#                 conn.close()
#
#                 if user:
#                     st.session_state.logged_in = True
#                     st.session_state.user_email = email
#                     st.session_state.user_team = team_name
#                     st.success(f"✅ Welcome, {email}! Redirecting to dashboard...")
#                     st.balloons()
#                     st.rerun()
#
#                 else:
#                     st.error("❌ Invalid email or team name. Try again.")
#             else:
#                 st.error("⚠️ Database connection failed.")
#
# # -------------------- DASHBOARD SECTION --------------------
# if st.session_state.logged_in:
#     st.success(f"👋 Logged in as **{st.session_state.user_email}** | Team: **{st.session_state.user_team}**")
#     st.markdown("<hr class='divider'>", unsafe_allow_html=True)
#
#     # --- Fetch Team Members ---
#     conn = get_db_connection()
#     team_members = []
#     if conn:
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("SELECT email FROM users WHERE team_name = %s", (st.session_state.user_team,))
#         team_members = [row["email"] for row in cursor.fetchall()]
#         cursor.close()
#         conn.close()
#
#     # --- Upload Transcript ---
#     st.markdown("<h2 class='section-header'>📄 Upload Meeting Transcript</h2>", unsafe_allow_html=True)
#     with st.expander("Click to upload and analyze your meeting transcript"):
#         uploaded_file = st.file_uploader("Choose a .docx file", type=["docx"])
#         analyze_clicked = st.button("🔍 Analyze Transcript")
#
#         if analyze_clicked and uploaded_file:
#             with st.spinner("🧠 Analyzing transcript... Please wait..."):
#                 try:
#                     analysis_result = analyze_meeting_docx(uploaded_file)
#                     if analysis_result.get("status") == "success":
#                         st.session_state.summary = analysis_result.get("content", "")
#                         st.balloons()
#                         st.success("✅ Analysis Complete!")
#                         st.text_area("📝 Meeting Summary", st.session_state.summary, height=200)
#                     else:
#                         st.error(analysis_result.get("message", "Error during analysis"))
#                 except Exception as e:
#                     st.error(f"❌ Analysis failed: {e}")
#
#     # --- Send Emails ---
#     if team_members:
#         st.markdown("<h2 class='section-header'>📧 Send Meeting Summary</h2>", unsafe_allow_html=True)
#         with st.expander("Click to view email options"):
#             recipients = st.multiselect("Select Recipients", team_members, default=team_members)
#             email_body = st.text_area("Email Content", st.session_state.get("summary", ""), height=150)
#             send_email_clicked = st.button("📨 Send Email")
#
#             if send_email_clicked and recipients:
#                 with st.spinner("✉️ Sending meeting summary..."):
#                     try:
#                         response = send_meeting_email(
#                             sender_email=st.session_state.user_email,
#                             recipients=recipients,
#                             subject="Meeting Summary",
#                             body=email_body
#                         )
#                         if response.get("status") == "success":
#                             st.success("✅ Emails sent successfully!")
#                             st.snow()
#                         else:
#                             st.error(response.get("message", "Error sending emails"))
#                     except Exception as e:
#                         st.error(f"❌ Failed to send emails: {e}")
#     else:
#         st.warning("⚠️ No team members found in your team.")
#
#     # --- Add Reminders ---
#     if st.session_state.summary:
#         st.markdown("<h2 class='section-header'>⏰ Add Reminders</h2>", unsafe_allow_html=True)
#         with st.expander("Click to add meeting tasks to shared calendar"):
#             add_reminders_clicked = st.button("🗓️ Add Reminders")
#             if add_reminders_clicked:
#                 with st.spinner("⏳ Adding reminders to team calendar..."):
#                     try:
#                         set_task_reminders(st.session_state.summary)
#                         st.success("✅ Reminders successfully added!")
#                         st.balloons()
#                     except Exception as e:
#                         st.error(f"❌ Failed to add reminders: {e}")
#
#     # --- Logout ---
#     st.markdown("<hr class='divider'>", unsafe_allow_html=True)
#     logout_col = st.columns([8, 2])
#     with logout_col[1]:
#         if st.button("🚪 Logout"):
#             st.session_state.logged_in = False
#             st.session_state.user_email = ""
#             st.session_state.user_team = ""
#             st.session_state.summary = ""
#             st.success("👋 Logged out successfully!")
#             st.rerun()



