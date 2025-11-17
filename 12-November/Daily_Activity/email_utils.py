# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import os
# from dotenv import load_dotenv
#
# load_dotenv()
#
# EMAIL_USER = os.getenv("EMAIL_USER")
# EMAIL_PASS = os.getenv("EMAIL_PASS")
#
# def send_email(subject, body, recipients):
#     """
#     Send email using Gmail SMTP to multiple recipients.
#     """
#     msg = MIMEMultipart()
#     msg["From"] = EMAIL_USER
#     msg["To"] = ", ".join(recipients)
#     msg["Subject"] = subject
#     msg.attach(MIMEText(body, "plain"))
#
#     try:
#         with smtplib.SMTP("smtp.gmail.com", 587) as server:
#             server.starttls()
#             server.login(EMAIL_USER, EMAIL_PASS)
#             server.sendmail(EMAIL_USER, recipients, msg.as_string())
#         print("✅ Emails sent successfully.")
#         return True
#     except Exception as e:
#         print(f"❌ Error sending email: {e}")
#         return False


import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def send_email(subject, body, recipients):
    """
    Send styled HTML email using Gmail SMTP to multiple recipients.
    `body` can contain plain text or HTML (from LLM analysis).
    """
    msg = MIMEMultipart("alternative")
    msg["From"] = EMAIL_USER
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject

    # Prepare plain text fallback and HTML content
    text_version = "Your email client does not support HTML content.\n\n" + body
    body_html = body.replace("\n", "<br>")

    html_version = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <h2 style="color:#2E86C1;">📋 Meeting Summary & MOM</h2>
        <div style="background-color:#f8f9f9;padding:15px;border-radius:8px;">
            {body_html}
        </div>
        <p style="margin-top:20px;">Best Regards,<br><b>Meeting Assistant 🤖</b></p>
      </body>
    </html>
    """

    # Attach both plain text and HTML versions
    msg.attach(MIMEText(text_version, "plain"))
    msg.attach(MIMEText(html_version, "html"))

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, recipients, msg.as_string())
        print(f"✅ Emails sent successfully to {', '.join(recipients)}.")
        return True
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False


if __name__ == "__main__":
    # 🧩 Quick local test
    recipients = ["bholeanushka1@gmail.com", "kalaburgirohit@gmail.com"]
    body = """
    ### Meeting Summary
    - Discussed Q4 goals and next steps.

    ### Minutes of Meeting
    - Reviewed project status
    - Assigned tasks to team members

    ### Action Items
    - Priya: Update model pipeline (Due 18 Nov)
    - Aniket: Finalize dashboard UI (Due 15 Nov)
    """
    send_email("📅 Meeting Summary Report", body, recipients)




