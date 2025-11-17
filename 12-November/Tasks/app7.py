# / *Welcome
# Section * /
# .welcome - section
# {
#     background: linear - gradient(135deg,  # 1a1f2e 0%, #16202d 100%);
# padding: 30
# px
# 40
# px;
# border - radius: 12
# px;
# margin - bottom: 40
# px;
# box - shadow: 0
# 4
# px
# 20
# px
# rgba(0, 0, 0, 0.4);
# border: 1
# px
# solid
# rgba(0, 212, 255, 0.1);
# }
#
# .welcome - title
# {
#     font - size: 32px;
# font - weight: 700;
# background: linear - gradient(135
# deg,  # 00d4ff, #7b68ee);
# -webkit - background - clip: text;
# -webkit - text - fill - color: transparent;
# background - clip: text;
# margin - bottom: 8
# px;
# }
#
# .welcome - subtitle
# {
#     font - size: 16px;
# color:  # b8c5d6;
# margin - bottom: 20
# px;
# }
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
    page_icon="🤖",
    initial_sidebar_state="collapsed"
)

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
    }

    body {
        background: #0f1419;
        color: #e8eef7;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }

    /* Top Bar Styling */
    .top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px 40px;
        background: linear-gradient(135deg, #1a1f2e 0%, #16202d 100%);
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.4);
        margin-bottom: 40px;
        border-radius: 0 0 12px 12px;
        border-bottom: 1px solid #2a3f5f;
    }

    .app-header {
        font-size: 24px;
        font-weight: 700;
        background: linear-gradient(135deg, #00d4ff, #7b68ee);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .user-info {
        display: flex;
        align-items: center;
        gap: 16px;
    }

    .user-badge {
        background: rgba(255, 255, 255, 0.08);
        padding: 8px 14px;
        border-radius: 8px;
        font-size: 13px;
        color: #b8c5d6;
        font-weight: 500;
        border: 1px solid rgba(0, 212, 255, 0.2);
    }

    .logout-btn {
        background: linear-gradient(135deg, #ff6b6b, #ee5a6f);
        color: #ffffff;
        padding: 8px 16px;
        border-radius: 6px;
        border: none;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 13px;
    }

    .logout-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(255, 107, 107, 0.3);
    }

    /* Main Container */
    .main-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 40px 40px;
    }

    /* Welcome Section */
    .welcome-section {
        background: white;
        padding: 30px 40px;
        border-radius: 12px;
        margin-bottom: 40px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
    }

    .welcome-title {
        font-size: 32px;
        font-weight: 700;
        color: #1e3799;
        margin-bottom: 8px;
    }

    .welcome-subtitle {
        font-size: 16px;
        color: #636e72;
        margin-bottom: 20px;
    }

    /* Flow Section */
    .flow-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin-top: 30px;
    }

    .flow-step {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        border-left: 4px solid #00d4ff;
        border: 1px solid rgba(0, 212, 255, 0.15);
        transition: all 0.3s ease;
    }

    .flow-step:hover {
        transform: translateY(-4px);
        background: rgba(0, 212, 255, 0.08);
        box-shadow: 0 8px 20px rgba(0, 212, 255, 0.2);
    }

    .step-number {
        font-size: 32px;
        font-weight: 700;
        color: #00d4ff;
        margin-bottom: 10px;
    }

    .step-title {
        font-size: 14px;
        font-weight: 600;
        color: #e8eef7;
    }

    .step-description {
        font-size: 12px;
        color: #b8c5d6;
        margin-top: 5px;
    }

    /* Card Styling */
    .stCard {
        background: linear-gradient(135deg, #1a1f2e 0%, #16202d 100%);
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        margin-bottom: 30px;
        border: 1px solid rgba(0, 212, 255, 0.15);
        border-top: 2px solid #00d4ff;
    }

    .section-header {
        font-size: 22px;
        color: #00d4ff;
        font-weight: 700;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    /* Teammate Tiles */
    .team-tiles-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
        gap: 16px;
        margin-top: 20px;
    }

    .teammate-tile {
        background: rgba(255, 255, 255, 0.05);
        padding: 16px;
        border-radius: 10px;
        border: 2px solid rgba(0, 212, 255, 0.2);
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .teammate-tile:hover {
        border-color: #00d4ff;
        box-shadow: 0 8px 20px rgba(0, 212, 255, 0.2);
        transform: translateY(-4px);
        background: rgba(0, 212, 255, 0.1);
    }

    .teammate-tile.selected {
        background: linear-gradient(135deg, #00d4ff, #7b68ee);
        color: white;
        border-color: #00d4ff;
        box-shadow: 0 8px 20px rgba(0, 212, 255, 0.3);
    }

    .teammate-avatar {
        font-size: 32px;
        margin-bottom: 10px;
    }

    .teammate-email {
        font-size: 13px;
        font-weight: 500;
        word-break: break-all;
        color: #b8c5d6;
    }

    .teammate-tile.selected .teammate-email {
        color: white;
    }

    /* Button Styling */
    .stButton > button {
        border-radius: 8px;
        background: linear-gradient(135deg, #00d4ff, #7b68ee);
        color: white;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
        padding: 12px 32px;
        font-size: 15px;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 212, 255, 0.3);
    }

    /* Selected Recipients Display */
    .selected-display {
        background: rgba(0, 212, 255, 0.08);
        padding: 16px;
        border-radius: 8px;
        margin-top: 20px;
        border-left: 4px solid #00d4ff;
        border: 1px solid rgba(0, 212, 255, 0.2);
    }

    .recipient-tag {
        display: inline-block;
        background: linear-gradient(135deg, #00d4ff, #7b68ee);
        color: white;
        padding: 6px 12px;
        border-radius: 20px;
        margin: 4px;
        font-size: 13px;
        font-weight: 500;
    }

    /* Text Area */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.05);
        color: #e8eef7;
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 8px;
        font-family: 'Monaco', monospace;
        font-size: 14px;
    }

    /* Success/Error Messages */
    .stSuccess, .stError, .stWarning {
        border-radius: 8px;
        padding: 16px;
    }

    /* Divider */
    .divider {
        border: none;
        height: 2px;
        background: linear-gradient(to right, #00d4ff, #7b68ee);
        margin: 30px 0;
    }

    /* Tagline */
    .tagline {
        font-size: 13px;
        color: #b8c5d6;
        font-weight: 500;
        margin-top: 8px;
    }

</style>
""", unsafe_allow_html=True)

# -------------------- SESSION STATE --------------------
for key in ["logged_in", "user_email", "user_team", "summary", "enhanced_email", "selected_recipients"]:
    if key not in st.session_state: \
    st.session_state[key] = [] if key == "selected_recipients" else ("" if key != "logged_in" else False)

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


# -------------------- LOGIN PAGE --------------------
if not st.session_state.logged_in:
    st.markdown("""
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("<div style='text-align: center; padding: 60px 0;'>", unsafe_allow_html=True)
        st.markdown("<h1 style='color: white; font-size: 48px; font-weight: 700;'>🤖 Smart Meeting Synthesizer</h1>",
                    unsafe_allow_html=True)
        st.markdown(
            "<p style='color: rgba(255,255,255,0.9); font-size: 18px; margin-bottom: 40px;'>Transform meetings into actionable intelligence</p>",
            unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            "<div style='background: white; padding: 40px; border-radius: 16px; box-shadow: 0 20px 60px rgba(0,0,0,0.3);'>",
            unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: #1e3799; margin-bottom: 30px;'>🔐 Employee Login</h2>",
                    unsafe_allow_html=True)

        email = st.text_input("📧 Email Address", placeholder="your.email@company.com").strip().lower()
        team_name = st.text_input("👥 Team Name", placeholder="Engineering").strip().lower()

        if st.button("Login", use_container_width=True):
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
                        st.error("❌ Invalid credentials. Check your email or team name.")
            except Exception as e:
                st.error(f"⚠️ Login failed due to: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

# -------------------- DASHBOARD --------------------
else:
    # --- Top Bar with Logout ---
    st.markdown(f"""
    <div class='top-bar'>
        <div class='app-header'>🤖 Smart Meeting Synthesizer</div>
        <div class='user-info'>
            <div class='user-badge'>👤 {st.session_state.user_email} | 👥 {st.session_state.user_team}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Logout button in top right
    col1, col2 = st.columns([0.95, 0.05])
    with col2:
        if st.button("🚪", help="Logout", key="logout_btn"):
            st.session_state.clear()
            st.rerun()

    # --- Main Container ---
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)

    # --- Welcome Section with Flow ---
    st.markdown("""
    <div class='welcome-section'>
        <div class='welcome-title'>Welcome to Your Meeting Hub</div>
        <div class='welcome-subtitle'>Streamline your meeting documentation process in just 5 simple steps</div>

        <div class='flow-container'>
            <div class='flow-step'>
                <div class='step-number'>1️⃣</div>
                <div class='step-title'>Upload Transcript</div>
                <div class='step-description'>Add your .docx meeting file</div>
            </div>
            <div class='flow-step'>
                <div class='step-number'>2️⃣</div>
                <div class='step-title'>AI Analysis</div>
                <div class='step-description'>Extract insights automatically</div>
            </div>
            <div class='flow-step'>
                <div class='step-number'>3️⃣</div>
                <div class='step-title'>Generate Summary</div>
                <div class='step-description'>Review meeting highlights</div>
            </div>
            <div class='flow-step'>
                <div class='step-number'>4️⃣</div>
                <div class='step-title'>Share with Team</div>
                <div class='step-description'>Send to teammates</div>
            </div>
            <div class='flow-step'>
                <div class='step-number'>5️⃣</div>
                <div class='step-title'>Set Reminders</div>
                <div class='step-description'>Track action items</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Fetch Team Members ---
    conn = get_db_connection()
    team_members = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT email FROM users WHERE team_name = %s", (st.session_state.user_team,))
        team_members = [row["email"] for row in cursor.fetchall()]
        cursor.close()
        conn.close()

    # --- Upload Transcript Section ---
    st.markdown("<div class='stCard'>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>📄 Step 1: Upload Meeting Transcript</div>", unsafe_allow_html=True)
    st.markdown("<p class='tagline'>📌 Upload a .docx file containing your meeting notes or transcript</p>",
                unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Choose meeting transcript", type=["docx"], label_visibility="collapsed")

    if st.button("🔍 Analyze Transcript", use_container_width=True):
        if uploaded_file:
            with st.spinner("🔍 Analyzing your meeting transcript..."):
                try:
                    result = analyze_meeting_docx(uploaded_file)
                    if result.get("status") == "success":
                        st.session_state.summary = result.get("content", "")
                        st.success("✅ Meeting summary generated successfully.")

                        st.markdown("<h3 class='section-header' style='margin-top: 30px;'>📋 Meeting Summary</h3>",
                                    unsafe_allow_html=True)
                        st.markdown("""
                        <div style='background: #f8f9fa; padding: 20px; border-radius: 8px; border-left: 4px solid #0984e3;'>
                        """, unsafe_allow_html=True)
                        st.write(st.session_state.summary)
                        st.markdown("</div>", unsafe_allow_html=True)

                        # Auto-enhance email after summary
                        with st.spinner("✨ Generating professional email draft..."):
                            enhanced = enhance_email_body(st.session_state.summary)
                            st.session_state.enhanced_email = enhanced or st.session_state.summary

                        st.markdown("<h3 class='section-header' style='margin-top: 30px;'>✉️ Email Draft</h3>",
                                    unsafe_allow_html=True)
                        st.session_state.enhanced_email = st.text_area(
                            "Edit your email",
                            st.session_state.enhanced_email,
                            height=250,
                            label_visibility="collapsed"
                        )
                    else:
                        st.error(result.get("message", "Error during analysis."))
                except Exception as e:
                    st.error(f"Analysis failed: {e}")
        else:
            st.warning("⚠️ Please upload a .docx file before analyzing.")
    st.markdown("</div>", unsafe_allow_html=True)

    # --- Email Sending Section ---
    if team_members and st.session_state.enhanced_email:
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'>✉️ Step 4: Share with Your Team</div>", unsafe_allow_html=True)
        st.markdown("<p class='tagline'>👥 Select team members to receive the meeting summary</p>",
                    unsafe_allow_html=True)

        # Display teammates as tiles
        st.markdown(
            "<p style='font-size: 14px; font-weight: 600; color: #2c3e50; margin-bottom: 16px;'>Select Recipients:</p>",
            unsafe_allow_html=True)

        cols = st.columns(len(team_members)) if len(team_members) <= 4 else st.columns(4)

        for idx, member in enumerate(team_members):
            with cols[idx % len(cols)]:
                is_selected = member in st.session_state.selected_recipients
                tile_class = "teammate-tile selected" if is_selected else "teammate-tile"

                if st.button(
                        f"👤\n{member.split('@')[0]}\n{member}",
                        key=f"tile_{member}",
                        use_container_width=True
                ):
                    if is_selected:
                        st.session_state.selected_recipients.remove(member)
                    else:
                        st.session_state.selected_recipients.append(member)
                    st.rerun()

        # Display selected recipients
        if st.session_state.selected_recipients:
            st.markdown("<div class='selected-display'>", unsafe_allow_html=True)
            st.markdown(
                f"<p style='font-weight: 600; margin-bottom: 12px;'>✅ Selected Recipients ({len(st.session_state.selected_recipients)}):</p>",
                unsafe_allow_html=True)
            for recipient in st.session_state.selected_recipients:
                st.markdown(f"<span class='recipient-tag'>{recipient}</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        if st.button("📤 Send Meeting Summary", use_container_width=True):
            if not st.session_state.selected_recipients:
                st.warning("⚠️ Please select at least one recipient.")
            else:
                with st.spinner("📨 Sending summary emails..."):
                    try:
                        response = send_meeting_email(
                            sender_email=st.session_state.user_email,
                            recipients=st.session_state.selected_recipients,
                            subject="Meeting Summary",
                            body=st.session_state.enhanced_email
                        )
                        if response.get("status") == "success":
                            st.success(
                                f"✅ Emails sent successfully to {len(st.session_state.selected_recipients)} recipient(s).")
                        else:
                            st.error(response.get("message", "Email sending failed."))
                    except Exception as e:
                        st.error(f"Email dispatch failed: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- Reminders Section ---
    if st.session_state.summary:
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'>⏰ Step 5: Add Follow-up Reminders</div>", unsafe_allow_html=True)
        st.markdown("<p class='tagline'>📅 Set reminders for action items and important follow-ups</p>",
                    unsafe_allow_html=True)

        if st.button("⏰ Add Reminders to Calendar", use_container_width=True):
            with st.spinner("🔄 Syncing reminders..."):
                try:
                    set_task_reminders(st.session_state.summary)
                    st.success("✅ Reminders added successfully to your calendar.")
                except Exception as e:
                    st.error(f"Failed to add reminders: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)