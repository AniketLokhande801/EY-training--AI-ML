# import os
# from datetime import datetime, timedelta
# import mysql.connector
# from mysql.connector import Error
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# from langchain_core.prompts import PromptTemplate
# from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv
#
# load_dotenv()
#
# # -------------------- Google Calendar --------------------
# SCOPES = ['https://www.googleapis.com/auth/calendar']
# SERVICE_ACCOUNT_FILE = "projectey-c8a5ee32b7cd.json"
#
# credentials = service_account.Credentials.from_service_account_file(
#     SERVICE_ACCOUNT_FILE, scopes=SCOPES
# )
#
# # -------------------- LLM to extract tasks --------------------
# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# llm = ChatOpenAI(
#     model="gpt-4o-mini",
#     temperature=0.3,
#     base_url="https://openrouter.ai/api/v1",
#     api_key=OPENROUTER_API_KEY,
# )
#
# task_extract_template = PromptTemplate(
#     input_variables=["analysis_text"],
#     template="""
# You are an AI assistant. Extract all tasks with assigned person(s) and deadlines from the following meeting analysis:
#
# {analysis_text}
#
# Output in JSON format:
# [
#     {{
#         "task": "...",
#         "person": "...",
#         "deadline": "..."  // if not mentioned, "Not specified"
#     }}
# ]
# """
# )
#
# # -------------------- Database --------------------
# DB_CONFIG = {
#     "host": "localhost",
#     "user": "root",
#     "password": "1234",
#     "database": "meeting_ai"
# }
#
# def get_email_by_name(name):
#     try:
#         conn = mysql.connector.connect(**DB_CONFIG)
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("SELECT email FROM users WHERE name=%s", (name,))
#         result = cursor.fetchone()
#         cursor.close()
#         conn.close()
#         if result:
#             return result['email']
#         return None
#     except Error as e:
#         print("DB Error:", e)
#         return None
#
# # -------------------- Calendar Event --------------------
# def create_google_calendar_event(email, task, deadline_str):
#     if deadline_str.lower() == "not specified":
#         print(f"⚠️ Skipping {task} for {email}: no deadline")
#         return
#
#     try:
#         # Parse date
#         deadline_dt = datetime.strptime(deadline_str, "%b %d").replace(year=datetime.now().year)
#         service = build('calendar', 'v3', credentials=credentials)
#         event = {
#             'summary': task,
#             'description': f'Reminder: {task}',
#             'start': {'dateTime': deadline_dt.isoformat(), 'timeZone': 'Asia/Kolkata'},
#             'end': {'dateTime': (deadline_dt + timedelta(hours=1)).isoformat(), 'timeZone': 'Asia/Kolkata'},
#             'attendees': [{'email': email}],
#             'reminders': {
#                 'useDefault': False,
#                 'overrides': [
#                     {'method': 'email', 'minutes': 60},
#                     {'method': 'popup', 'minutes': 30},
#                 ],
#             },
#         }
#         service.events().insert(calendarId=email, body=event).execute()
#         print(f"✅ Reminder set for {email} | Task: {task} | Deadline: {deadline_str}")
#     except Exception as e:
#         print("Google Calendar Error:", e)
#
# # -------------------- Main Function --------------------
# def set_task_reminders(analysis_text):
#     # Step 1: Extract tasks using LLM
#     result = llm.invoke(task_extract_template.format(analysis_text=analysis_text))
#     tasks_json = result.content
#
#     import json
#     try:
#         tasks = json.loads(tasks_json)
#     except Exception as e:
#         print("Failed to parse LLM JSON:", e)
#         return
#
#     # Step 2: For each task, get email and create reminder
#     for t in tasks:
#         task_name = t.get("task")
#         person = t.get("person")
#         deadline = t.get("deadline", "Not specified")
#         email = get_email_by_name(person)
#         if email:
#             create_google_calendar_event(email, task_name, deadline)
#         else:
#             print(f"⚠️ No email found for {person}")
#
#
#
#

# import os
# from datetime import datetime, timedelta
# import mysql.connector
# from mysql.connector import Error
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# from langchain_core.prompts import PromptTemplate
# from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv
# import json
# import re
#
# load_dotenv()
#
# # -------------------- Google Calendar --------------------
# SCOPES = ['https://www.googleapis.com/auth/calendar']
# SERVICE_ACCOUNT_FILE = "projectey-c8a5ee32b7cd.json"
#
# credentials = service_account.Credentials.from_service_account_file(
#     SERVICE_ACCOUNT_FILE, scopes=SCOPES
# )
#
# # -------------------- LLM to extract tasks --------------------
# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# llm = ChatOpenAI(
#     model="gpt-4o-mini",
#     temperature=0.3,
#     base_url="https://openrouter.ai/api/v1",
#     api_key=OPENROUTER_API_KEY,
# )
#
# task_extract_template = PromptTemplate(
#     input_variables=["analysis_text"],
#     template="""
# You are an AI assistant. Extract all tasks with assigned person(s) and deadlines from the following meeting analysis:
#
# {analysis_text}
#
# Output in JSON format (list of objects):
# [
#     {{
#         "task": "...",
#         "person": "...",
#         "deadline": "..."  // if not mentioned, "Not specified"
#     }}
# ]
# """
# )
#
# # -------------------- Database --------------------
# DB_CONFIG = {
#     "host": "localhost",
#     "user": "root",
#     "password": "1234",
#     "database": "meeting_ai"
# }
#
# def get_email_by_name(name):
#     try:
#         conn = mysql.connector.connect(**DB_CONFIG)
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("SELECT email FROM users WHERE name=%s", (name,))
#         result = cursor.fetchone()
#         cursor.close()
#         conn.close()
#         return result['email'] if result else None
#     except Error as e:
#         print("DB Error:", e)
#         return None
#
# # -------------------- Calendar Event --------------------
# def create_google_calendar_event(email, task, deadline_str):
#     if not deadline_str or deadline_str.lower() == "not specified":
#         print(f"⚠️ Skipping {task} for {email}: no deadline")
#         return
#
#     try:
#         # Convert date string like 'Nov 14' to datetime
#         deadline_dt = datetime.strptime(deadline_str, "%b %d").replace(year=datetime.now().year)
#         service = build('calendar', 'v3', credentials=credentials)
#         event = {
#             'summary': task,
#             'description': f'Reminder: {task}',
#             'start': {'dateTime': deadline_dt.isoformat(), 'timeZone': 'Asia/Kolkata'},
#             'end': {'dateTime': (deadline_dt + timedelta(hours=1)).isoformat(), 'timeZone': 'Asia/Kolkata'},
#             'attendees': [{'email': email}],
#             'reminders': {
#                 'useDefault': False,
#                 'overrides': [
#                     {'method': 'email', 'minutes': 60},
#                     {'method': 'popup', 'minutes': 30},
#                 ],
#             },
#         }
#         service.events().insert(calendarId=email, body=event).execute()
#         print(f"✅ Reminder set for {email} | Task: {task} | Deadline: {deadline_str}")
#     except Exception as e:
#         print("Google Calendar Error:", e)
#
# # -------------------- Main Function --------------------
# def set_task_reminders(analysis_text):
#     # Step 1: Extract tasks using LLM
#     result = llm.invoke(task_extract_template.format(analysis_text=analysis_text))
#     llm_output = result.content
#
#     # Remove code fences like ```json ... ```
#     cleaned = re.sub(r"^```.*?\n|```$", "", llm_output.strip(), flags=re.DOTALL)
#
#     # Step 2: Parse JSON
#     try:
#         tasks = json.loads(cleaned)
#     except Exception as e:
#         print("Failed to parse LLM JSON:", e)
#         return
#
#     # Step 3: For each task, get email and create reminder
#     for t in tasks:
#         task_name = t.get("task")
#         person = t.get("person")
#         deadline = t.get("deadline", "Not specified")
#         email = get_email_by_name(person)
#         if email:
#             create_google_calendar_event(email, task_name, deadline)
#         else:
#             print(f"⚠️ No email found for {person}")


# import os
# import re
# import json
# from datetime import datetime, timedelta
# import mysql.connector
# from mysql.connector import Error
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# from langchain_core.prompts import PromptTemplate
# from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv
#
# load_dotenv()
#
# # -------------------- Google Calendar --------------------
# SCOPES = ['https://www.googleapis.com/auth/calendar']
# SERVICE_ACCOUNT_FILE = "projectey-c8a5ee32b7cd.json"
#
# credentials = service_account.Credentials.from_service_account_file(
#     SERVICE_ACCOUNT_FILE, scopes=SCOPES
# )
#
# # Shared Calendar ID
# SHARED_CALENDAR_ID = "9bfba2b11a7fcf8a66a4664a9fb663421b2d925ce14bb9d5fcbf16867cf8c6a2@group.calendar.google.com"
#
# # -------------------- LLM to extract tasks --------------------
# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# llm = ChatOpenAI(
#     model="gpt-4o-mini",
#     temperature=0.3,
#     base_url="https://openrouter.ai/api/v1",
#     api_key=OPENROUTER_API_KEY,
# )
#
# task_extract_template = PromptTemplate(
#     input_variables=["analysis_text"],
#     template="""
# You are an AI assistant. Extract all tasks with assigned person(s) and deadlines from the following meeting analysis:
#
# {analysis_text}
#
# Output in JSON format (list of objects):
# [
#     {{
#         "task": "...",
#         "person": "...",
#         "deadline": "..."  // if not mentioned, "Not specified"
#     }}
# ]
# """
# )
#
# # -------------------- Database --------------------
# DB_CONFIG = {
#     "host": "localhost",
#     "user": "root",
#     "password": "1234",
#     "database": "meeting_ai"
# }
#
# def get_email_by_name(name):
#     """Fetch email from DB for given person name."""
#     try:
#         conn = mysql.connector.connect(**DB_CONFIG)
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("SELECT email FROM users WHERE name=%s", (name,))
#         result = cursor.fetchone()
#         cursor.close()
#         conn.close()
#         return result['email'] if result else None
#     except Error as e:
#         print("DB Error:", e)
#         return None
#
# # -------------------- Calendar Event --------------------
# def create_google_calendar_event(task, deadline_str, attendees_emails):
#     """Create a Google Calendar event in the shared calendar."""
#     if not deadline_str or deadline_str.lower() == "not specified":
#         print(f"⚠️ Skipping {task}: no deadline")
#         return
#
#     try:
#         # Convert date string like 'Nov 14' to datetime
#         deadline_dt = datetime.strptime(deadline_str, "%b %d").replace(year=datetime.now().year)
#         service = build('calendar', 'v3', credentials=credentials)
#
#         event = {
#             'summary': task,
#             'description': f'Reminder: {task}',
#             'start': {'dateTime': deadline_dt.isoformat(), 'timeZone': 'Asia/Kolkata'},
#             'end': {'dateTime': (deadline_dt + timedelta(hours=1)).isoformat(), 'timeZone': 'Asia/Kolkata'},
#             'attendees': [{'email': email} for email in attendees_emails],
#             'reminders': {
#                 'useDefault': False,
#                 'overrides': [
#                     {'method': 'email', 'minutes': 60},
#                     {'method': 'popup', 'minutes': 30},
#                 ],
#             },
#         }
#
#         service.events().insert(calendarId=SHARED_CALENDAR_ID, body=event).execute()
#         print(f"✅ Reminder set for {', '.join(attendees_emails)} | Task: {task} | Deadline: {deadline_str}")
#     except Exception as e:
#         print("Google Calendar Error:", e)
#
# # -------------------- Main Function --------------------
# def set_task_reminders(analysis_text):
#     """
#     Process LLM meeting analysis, extract tasks,
#     fetch emails, and create reminders in the shared calendar.
#     """
#     # Step 1: Extract tasks using LLM
#     result = llm.invoke(task_extract_template.format(analysis_text=analysis_text))
#     llm_output = result.content
#
#     # Step 2: Clean LLM output (remove ```json fences)
#     cleaned = re.sub(r"^```.*?\n|```$", "", llm_output.strip(), flags=re.DOTALL)
#
#     # Step 3: Parse JSON
#     try:
#         tasks = json.loads(cleaned)
#     except Exception as e:
#         print("Failed to parse LLM JSON:", e)
#         return
#
#     # Step 4: For each task, get email(s) and create reminder
#     for t in tasks:
#         task_name = t.get("task")
#         person = t.get("person")
#         deadline = t.get("deadline", "Not specified")
#         email = get_email_by_name(person)
#         if email:
#             create_google_calendar_event(task_name, deadline, [email])
#         else:
#             print(f"⚠️ No email found for {person}")


import os
from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import Error
from google.oauth2 import service_account
from googleapiclient.discovery import build
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import json
import re

load_dotenv()

# -------------------- Google Calendar --------------------
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = "projectey-c8a5ee32b7cd.json"

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# Shared Calendar ID
SHARED_CALENDAR_ID = "9bfba2b11a7fcf8a66a4664a9fb663421b2d925ce14bb9d5fcbf16867cf8c6a2@group.calendar.google.com"

# -------------------- LLM to extract tasks --------------------
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3,
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

task_extract_template = PromptTemplate(
    input_variables=["analysis_text"],
    template="""
You are an AI assistant. Extract all tasks with assigned person(s) and deadlines from the following meeting analysis:

{analysis_text}

Output in JSON format (list of objects):
[
    {{
        "task": "...",
        "person": "...",
        "deadline": "..."  // if not mentioned, "Not specified"
    }}
]
"""
)

# -------------------- Database --------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "meeting_ai"
}

def get_email_by_name(name):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT email FROM users WHERE name=%s", (name,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result['email'] if result else None
    except Error as e:
        print("DB Error:", e)
        return None

# -------------------- Calendar Event --------------------
def create_google_calendar_event(person, task, deadline_str):
    if not deadline_str or deadline_str.lower() == "not specified":
        print(f"⚠️ Skipping {task} for {person}: no deadline")
        return

    try:
        # Convert date string like 'Nov 14' to datetime
        deadline_dt = datetime.strptime(deadline_str, "%b %d").replace(year=datetime.now().year)
        service = build('calendar', 'v3', credentials=credentials)
        event = {
            'summary': task,
            'description': f"Assigned to {person}: {task}",
            'start': {'dateTime': deadline_dt.isoformat(), 'timeZone': 'Asia/Kolkata'},
            'end': {'dateTime': (deadline_dt + timedelta(hours=1)).isoformat(), 'timeZone': 'Asia/Kolkata'},
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 30}
                ],
            },
        }
        service.events().insert(calendarId=SHARED_CALENDAR_ID, body=event).execute()
        print(f"✅ Reminder added in shared calendar | {person} | {task} | Deadline: {deadline_str}")
    except Exception as e:
        print("Google Calendar Error:", e)

# -------------------- Main Function --------------------
def set_task_reminders(analysis_text):
    # Step 1: Extract tasks using LLM
    result = llm.invoke(task_extract_template.format(analysis_text=analysis_text))
    llm_output = result.content

    # Remove code fences like ```json ... ```
    cleaned = re.sub(r"^```.*?\n|```$", "", llm_output.strip(), flags=re.DOTALL)

    # Step 2: Parse JSON
    try:
        tasks = json.loads(cleaned)
    except Exception as e:
        print("Failed to parse LLM JSON:", e)
        return

    # Step 3: Create reminders in shared calendar
    for t in tasks:
        task_name = t.get("task")
        person = t.get("person")
        deadline = t.get("deadline", "Not specified")
        create_google_calendar_event(person, task_name, deadline)

