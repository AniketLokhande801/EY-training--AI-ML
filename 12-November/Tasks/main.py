# # from fastapi import FastAPI, Form
# # from fastapi import FastAPI, UploadFile, File
# # from fastapi.middleware.cors import CORSMiddleware
# # import mysql.connector
# # from mysql.connector import Error
# # from llm_service import analyze_meeting_docx
# #
# # app = FastAPI(title="Meeting AI Assistant")
# #
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )
# #
# # # ---------- MySQL Connection Function ----------
# # def get_db_connection():
# #     try:
# #         conn = mysql.connector.connect(
# #             host="localhost",
# #             user="root",
# #             password="1234",
# #             database="meeting_ai"
# #         )
# #         return conn
# #     except Error as e:
# #         print("❌ Database connection error:", e)
# #         return None
# #
# #
# # # ---------- Test API: Check if User Exists ----------
# # @app.post("/check_user/")
# # def check_user(email: str = Form(...), team_name: str = Form(...)):
# #     conn = get_db_connection()
# #     if not conn:
# #         return {"error": "Failed to connect to database"}
# #
# #     cursor = conn.cursor(dictionary=True)
# #     query = "SELECT * FROM users WHERE email = %s AND team_name = %s"
# #     cursor.execute(query, (email, team_name))
# #     result = cursor.fetchone()
# #
# #     cursor.close()
# #     conn.close()
# #
# #     if result:
# #         return {"status": "success", "message": f"✅ User found in {team_name}", "user": result}
# #     else:
# #         return {"status": "error", "message": "❌ User not found or team mismatch"}
# #
# #
# #
# # @app.post("/analyze_meeting/")
# # async def analyze_meeting(file: UploadFile = File(...)):
# #     try:
# #         result = analyze_meeting_docx(file)
# #         return result
# #     except Exception as e:
# #         return {"status": "error", "message": str(e)}
# #
# # from fastapi import Request
# # from email_service import send_meeting_email
# #
# # # ---------- Fetch Team Members (for Checkbox List) ----------
# # @app.get("/get_team_members/")
# # def get_team_members(team_name: str):
# #     """
# #     Fetch all emails in a given team so frontend can show them with checkboxes.
# #     """
# #     conn = get_db_connection()
# #     if not conn:
# #         return {"status": "error", "message": "Database connection failed"}
# #
# #     cursor = conn.cursor(dictionary=True)
# #     cursor.execute("SELECT email FROM users WHERE team_name = %s", (team_name,))
# #     members = [row["email"] for row in cursor.fetchall()]
# #
# #     cursor.close()
# #     conn.close()
# #
# #     if members:
# #         return {"status": "success", "team_name": team_name, "members": members}
# #     else:
# #         return {"status": "error", "message": "No members found for this team"}
# #
# #
# # # ---------- Send Email to Selected Members ----------
# # @app.post("/send_emails/")
# # async def send_emails(request: Request):
# #     """
# #     Accepts sender email, list of recipients, subject, and content body from frontend.
# #     Sends HTML formatted email via SMTP.
# #     """
# #     try:
# #         data = await request.json()
# #         sender_email = data.get("sender_email")
# #         recipients = data.get("recipients", [])
# #         subject = data.get("subject", "Meeting Summary & Minutes")
# #         body = data.get("body", "")
# #
# #         if not sender_email or not recipients or not body:
# #             return {"status": "error", "message": "Missing required fields"}
# #
# #         response = send_meeting_email(sender_email, recipients, subject, body)
# #         return response
# #
# #     except Exception as e:
# #         return {"status": "error", "message": str(e)}
# #
# #
# from fastapi import FastAPI, Form, UploadFile, File, Request
# from fastapi.middleware.cors import CORSMiddleware
# import mysql.connector
# from mysql.connector import Error
# from llm_service import analyze_meeting_docx
# from email_service import send_meeting_email
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse
#
#
# app = FastAPI(title="Meeting AI Assistant")
# app.mount("/static", StaticFiles(directory="static"), name="static")
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# @app.get("/")
# def root():
#     return FileResponse("templates/login.html")
#
#
# @app.get("/dashboard.html")
# def dashboard_page():
#     return FileResponse("templates/dashboard.html")
# # ---------- MySQL Connection Function ----------
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
#         print("❌ Database connection error:", e)
#         return None
#
#
# # ---------- 1️⃣ Check if User Exists ----------
# @app.post("/check_user/")
# def check_user(email: str = Form(...), team_name: str = Form(...)):
#     conn = get_db_connection()
#     if not conn:
#         return {"error": "Failed to connect to database"}
#
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM users WHERE email = %s AND team_name = %s", (email, team_name))
#     result = cursor.fetchone()
#
#     cursor.close()
#     conn.close()
#
#     if result:
#         return {"status": "success", "message": f"✅ User found in {team_name}", "user": result}
#     else:
#         return {"status": "error", "message": "❌ User not found or team mismatch"}
#
#
# # ---------- 2️⃣ Analyze Meeting Transcript ----------
# @app.post("/analyze_meeting/")
# async def analyze_meeting(file: UploadFile = File(...)):
#     try:
#         result = await analyze_meeting_docx(file)
#         return result
#     except Exception as e:
#         return {"status": "error", "message": str(e)}
#
#
# # ---------- 3️⃣ Fetch Team Members ----------
# @app.get("/get_team_members/")
# def get_team_members(team_name: str):
#     conn = get_db_connection()
#     if not conn:
#         return {"status": "error", "message": "Database connection failed"}
#
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT email FROM users WHERE team_name = %s", (team_name,))
#     members = [row["email"] for row in cursor.fetchall()]
#
#     cursor.close()
#     conn.close()
#
#     if members:
#         return {"status": "success", "team_name": team_name, "members": members}
#     else:
#         return {"status": "error", "message": "No members found for this team"}
#
#
# # ---------- 4️⃣ Send Email ----------
# @app.post("/send_emails/")
# async def send_emails(request: Request):
#     try:
#         data = await request.json()
#         sender_email = data.get("sender_email")
#         recipients = data.get("recipients", [])
#         subject = data.get("subject", "Meeting Summary & Minutes")
#         body = data.get("body", "")
#
#         if not sender_email or not recipients or not body:
#             return {"status": "error", "message": "Missing required fields"}
#
#         response = send_meeting_email(sender_email, recipients, subject, body)
#         return response
#
#     except Exception as e:
#         return {"status": "error", "message": str(e)}


from fastapi import FastAPI, Form, UploadFile, File, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import mysql.connector
from mysql.connector import Error
from llm_service import analyze_meeting_docx
from email_service import send_meeting_email
from reminder_service import set_task_reminders
import markdown

app = FastAPI(title="Meeting AI Assistant")

# Static and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ---------- Database ----------
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
        print("Database connection error:", e)
        return None

# ---------- Login page ----------
@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": ""})

# ---------- Handle login ----------
@app.post("/login/", response_class=HTMLResponse)
def login(request: Request, email: str = Form(...), team_name: str = Form(...)):
    conn = get_db_connection()
    if not conn:
        return templates.TemplateResponse("login.html", {"request": request, "error": "DB connection failed"})
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s AND team_name=%s", (email, team_name))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        return RedirectResponse(url=f"/dashboard/?email={email}&team={team_name}", status_code=302)
    else:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid email or team name"})

# ---------- Dashboard ----------
@app.get("/dashboard/", response_class=HTMLResponse)
def dashboard(request: Request, email: str, team: str):
    conn = get_db_connection()
    if not conn:
        return HTMLResponse("<h1>DB connection failed</h1>")
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT email FROM users WHERE team_name=%s", (team,))
    members = [row["email"] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "email": email, "team": team, "members": members, "message": ""}
    )

# ---------- Upload & Analyze ----------
# @app.post("/analyze_meeting/", response_class=HTMLResponse)
# def analyze_meeting(request: Request, email: str = Form(...), team: str = Form(...), file: UploadFile = File(...)):
#     try:
#         result = analyze_meeting_docx(file)  # Must return a string summary
#     except Exception as e:
#         result = f"Error analyzing file: {str(e)}"
#
#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT email FROM users WHERE team_name=%s", (team,))
#     members = [row["email"] for row in cursor.fetchall()]
#     cursor.close()
#     conn.close()
#
#     return templates.TemplateResponse(
#         "dashboard.html",
#         {"request": request, "email": email, "team": team, "members": members, "summary": result, "message": ""}
#     )

@app.post("/analyze_meeting/", response_class=HTMLResponse)
async def analyze_meeting(request: Request, email: str = Form(...), team: str = Form(...),
                          file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        result = analyze_meeting_docx(file_bytes, filename=file.filename)
    except Exception as e:
        result = {"status": "error", "content": f"Error analyzing file: {str(e)}"}

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT email FROM users WHERE team_name=%s", (team,))
    members = [row["email"] for row in cursor.fetchall()]
    cursor.close()
    conn.close()


    # After getting result from LLM
    html_summary = markdown.markdown(result.get("content", ""))
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "email": email,
        "team": team,
        "members": members,
        "summary": html_summary,
        "message": "" if result["status"] == "success" else result["content"]
    })



# ---------- Send Email ----------
@app.post("/send_emails/", response_class=HTMLResponse)
def send_emails(
    request: Request,
    email: str = Form(...),
    team: str = Form(...),
    recipients: str = Form(...),  # comma-separated emails
    summary: str = Form(...)
):
    try:
        recipient_list = [r.strip() for r in recipients.split(",") if r.strip()]
        send_meeting_email(email, recipient_list, "Meeting Summary", summary)
        message = "✅ Email sent successfully!"
    except Exception as e:
        message = f"Error sending email: {str(e)}"

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT email FROM users WHERE team_name=%s", (team,))
    members = [row["email"] for row in cursor.fetchall()]
    cursor.close()
    conn.close()

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "email": email, "team": team, "members": members, "summary": summary, "message": message}
    )

# ---------- Set Reminders ----------
@app.post("/set_reminders/", response_class=HTMLResponse)
def set_reminders(
    request: Request,
    email: str = Form(...),
    team: str = Form(...),
    summary: str = Form(...)
):
    try:
        # Call reminder service
        set_task_reminders(summary)
        message = "✅ Reminders successfully added to shared calendar!"
    except Exception as e:
        message = f"Error setting reminders: {str(e)}"

    # Reload team members for dashboard
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT email FROM users WHERE team_name=%s", (team,))
    members = [row["email"] for row in cursor.fetchall()]
    cursor.close()
    conn.close()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "email": email,
            "team": team,
            "members": members,
            "summary": summary,
            "message": message
        }
    )


