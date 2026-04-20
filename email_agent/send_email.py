
import smtplib
from email.message import EmailMessage
import os


def send_resume_email(
    to_email,
    subject,
    body,
    resume_path
):
    sender_email = os.getenv("SENDER_EMAIL")
    app_password = os.getenv("EMAIL_APP_PASSWORD")

    if not sender_email or not app_password:
        raise RuntimeError("Email credentials not set in environment variables")

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    # Attach Resume
    with open(resume_path, "rb") as f:
        resume_data = f.read()
        resume_name = os.path.basename(resume_path)

    msg.add_attachment(
        resume_data,
        maintype="application",
        subtype="pdf",
        filename=resume_name
    )

    # Send email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.send_message(msg)

    print(f"✅ Resume sent successfully to {to_email}")
