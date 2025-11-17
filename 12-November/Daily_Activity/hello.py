import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# Load from .env
load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def send_test_email():
    sender = EMAIL_USER
    receiver = "bholeanushka1@gmail.com"  # 🧠 Replace with your test email
    subject = "✅ SMTP Test - FastAPI Meeting Tool"
    body = """Hello!
This is a test email sent via Python SMTP.
If you received this, SMTP setup works fine!
"""

    # Create email
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Connect to Gmail SMTP
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(sender, receiver, message.as_string())
        print("✅ Email sent successfully!")
    except Exception as e:
        print("❌ Failed to send email:", e)

if __name__ == "__main__":
    send_test_email()
