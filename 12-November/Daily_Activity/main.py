# from fastapi import FastAPI, UploadFile, Form
# from fastapi.middleware.cors import CORSMiddleware
# from langchain_community.document_loaders import Docx2txtLoader
# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import PromptTemplate
# from dotenv import load_dotenv
# from email_utils import send_email
# import os
#
# # Load environment variables
# load_dotenv()
#
# app = FastAPI(title="Meeting Analyzer API")
#
# # Enable CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
# # LLM setup
# api_key = os.getenv("OPENROUTER_API_KEY")
#
# llm = ChatOpenAI(
#     model="gpt-4o-mini",
#     openai_api_key=api_key,
#     openai_api_base="https://openrouter.ai/api/v1"
# )
#
# # Prompt Template
# prompt_template = PromptTemplate(
#     input_variables=["meeting_text"],
#     template="""
# You are an AI meeting analyst. Analyze the meeting transcript below and provide the following three structured outputs:
#
# 1. **Concise Meeting Summary**: Capture the overall discussion, decisions, and key points.
# 2. **Detailed Minutes of Meeting (MOM)**: Include topics discussed, decisions made, and next steps.
# 3. **List of Action Items**: Extract tasks with assigned persons and deadlines (if mentioned).
#
# Meeting Transcript:
# {meeting_text}
#
# Format your response in clear sections with markdown headings:
# ### Meeting Summary
# ### Minutes of Meeting
# ### Action Items
# """
# )
#
# # -------------------------------
# # 1️⃣ Upload + Analyze Meeting File
# # -------------------------------
# @app.post("/analyze_meeting/")
# async def analyze_meeting(file: UploadFile):
#     """
#     Upload a .docx meeting file, analyze with LLM,
#     and return structured content (summary, MOM, action items).
#     """
#     # Save temporary file
#     temp_path = f"temp_{file.filename}"
#     with open(temp_path, "wb") as f:
#         f.write(await file.read())
#
#     # Load transcript
#     loader = Docx2txtLoader(temp_path)
#     docs = loader.load()
#     os.remove(temp_path)
#
#     meeting_text = docs[0].page_content
#
#     # Generate AI analysis
#     prompt = prompt_template.format(meeting_text=meeting_text)
#     result = llm.invoke(prompt)
#
#     return {
#         "status": "success",
#         "content": result.content
#     }
#
# # -------------------------------
# # 2️⃣ Send Email with LLM Summary
# # -------------------------------
# @app.post("/send_emails/")
# async def send_emails(
#     subject: str = Form(...),
#     body: str = Form(...),
#     recipients: str = Form(...)
# ):
#     """
#     Send the AI-generated meeting summary and MOM
#     to multiple recipients via HTML email.
#     """
#     recipient_list = [e.strip() for e in recipients.split(",") if e.strip()]
#     if not recipient_list:
#         return {"status": "error", "message": "No recipients provided"}
#
#     send_status = send_email(subject, body, recipient_list)
#
#     return {
#         "status": "success" if send_status else "error",
#         "message": "Emails sent successfully!" if send_status else "Failed to send emails"
#     }



from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from langchain_community.document_loaders import Docx2txtLoader
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from email_utils import send_email
import os

load_dotenv()

app = FastAPI(title="Meeting Analyzer API")

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- LLM Config ---
api_key = os.getenv("OPENROUTER_API_KEY")

llm = ChatOpenAI(
    model="gpt-4o-mini",
    openai_api_key=api_key,
    openai_api_base="https://openrouter.ai/api/v1"
)

prompt_template = PromptTemplate(
    input_variables=["meeting_text"],
#     template="""
# You are an AI meeting analyst. Analyze the meeting transcript below and provide the following three structured outputs:
#
# 1. **Concise Meeting Summary**
# 2. **Detailed Minutes of Meeting (MOM)**
# 3. **List of Action Items**
#
# Meeting Transcript:
# {meeting_text}
#
# Format the response clearly with markdown headings:
# ### Meeting Summary
# ### Minutes of Meeting
# ### Action Items
# """
    template="""
You are an AI Meeting Analyst Assistant. 
Analyze the following meeting transcript and provide a professional, clearly structured summary suitable for sending as an email. 
Avoid using markdown formatting, symbols, or tables. 
Use only plain text and bullet points for clarity.
 
Your response should have the following three sections in the exact order:
 
1. MEETING SUMMARY  
   - Give a concise overview (4–6 sentences) covering meeting objectives, key discussions, and decisions.
 
2. MINUTES OF MEETING  
   - List important discussion points and decisions as bullet points.  
   - For each item, include: topic, key insights, responsible person, and deadline (if available).
 
3. ACTION ITEMS  
   - List follow-up tasks as bullet points.  
   - Each bullet should include task description, responsible person, and due date (if mentioned).
 
If some details (like names or deadlines) are missing, just write "Not specified".
 
Meeting Transcript:
{meeting_text}
"""
)

# --- Endpoint: Analyze Transcript ---
@app.post("/analyze_meeting/")
async def analyze_meeting(file: UploadFile):
    """Step 1: Upload and analyze transcript"""
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    loader = Docx2txtLoader(temp_path)
    docs = loader.load()
    os.remove(temp_path)

    meeting_text = docs[0].page_content
    prompt = prompt_template.format(meeting_text=meeting_text)
    result = llm.invoke(prompt)

    return {"status": "success", "content": result.content}


# --- Endpoint: Send Emails ---
@app.post("/send_emails/")
async def send_emails(
    emails: str = Form(...),
    content: str = Form(...),
    subject: str = Form("📋 Meeting Summary, MOM & Action Items")
):
    """Step 2: Send email summary to recipients"""
    recipients = [e.strip() for e in emails.split(",") if e.strip()]
    if not recipients:
        return {"status": "error", "message": "No recipients provided"}

    send_status = send_email(subject, content, recipients)

    return {
        "status": "success" if send_status else "error",
        "recipients": recipients,
        "message": "Email sent successfully!" if send_status else "Email sending failed!"
    }
