
from email_agent.send_email import send_resume_email
from email_agent.email_body import generate_email_body
from email_agent.approval import get_manual_approval

job_title = "Construction Manager"
company_name = "Balfour Beatty"

subject = f"Application for {job_title}"
body = generate_email_body(job_title, company_name)

approved = get_manual_approval(
    job_title=job_title,
    company_name=company_name,
    subject=subject,
    body=body
)

if approved:
    send_resume_email(
        to_email="hr@example.com",   # replace with real HR email
        subject=subject,
        body=body,
        resume_path=r"C:\GITHUB\JobSearch\resume.pdf"
    )
else:
    print("❌ Email NOT sent (user cancelled)")

