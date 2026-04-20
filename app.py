
import streamlit as st
import os
from resume_reader.resume_reader import extract_resume_text
from skill_extractor.extract_skills import extract_skills
from job_search.live_jobs import fetch_jobs_live
from ai_matcher.matcher import rank_jobs
from email_agent.send_email import send_resume_email
from email_agent.email_body import generate_email_body
from email_agent.email_suggester import suggest_hr_emails

st.set_page_config(page_title="AI Job Application Assistant", layout="wide")

st.title("🤖 AI Job Application Assistant")
st.write("Search jobs, review matches, preview emails, and send your resume safely.")

# ---------------- Sidebar ----------------
st.sidebar.header("Settings")

location = st.sidebar.text_input("Job Location", value="London")


RESUME_PATH = "temp_resume.pdf"

uploaded_resume = st.sidebar.file_uploader(
    "Upload your resume (PDF) — upload once",
    type=["pdf"]
)

if uploaded_resume:
    with open(RESUME_PATH, "wb") as f:
        f.write(uploaded_resume.getbuffer())
    st.sidebar.success("✅ Resume uploaded and saved")

elif os.path.exists(RESUME_PATH):
    st.sidebar.info("📄 Using previously uploaded resume")

else:
    st.warning("Please upload your resume to continue.")
    st.stop()

# Always use the saved resume
resume_text = extract_resume_text(RESUME_PATH)
skills = extract_skills(resume_text)

st.sidebar.subheader("Extracted Skills")
st.sidebar.write(", ".join(skills))


# ---------------- Fetch jobs ----------------
if st.button("🔍 Find Matching Jobs"):
    with st.spinner("Searching jobs..."):
        jobs = fetch_jobs_live(skills, location)
        results = rank_jobs(resume_text, jobs)
        st.session_state["results"] = results

# ---------------- Display results ----------------
if "results" in st.session_state:
    st.subheader("🏆 Job Matches")

    for idx, job in enumerate(st.session_state["results"], start=1):
        job_id = f"{job['title']}|{job['company']}"

        with st.expander(f"{idx}. {job['title']} @ {job['company']}"):

            st.write(f"**Match Score:** {job['score']}%")
            st.write(f"**Matched Skills:** {', '.join(job['matched_skills'])}")

            st.subheader("📧 Suggested HR Emails")

            suggested_emails = suggest_hr_emails(
                job["company"],
                domain="co.uk"
            )

            selected_email = st.selectbox(
                "Choose HR email",
                options=suggested_emails,
                key=f"email_{idx}"
            )

            custom_email = st.text_input(
                "Or enter a custom email",
                value=selected_email,
                key=f"custom_email_{idx}"
            )

            subject = f"Application for {job['title']}"
            email_body = generate_email_body(job["title"], job["company"])

            st.subheader("📨 Email Preview")
            st.text_area(
                "Email body",
                value=email_body,
                height=220,
                key=f"body_{idx}"
            )

            if st.button(f"✅ Send Resume", key=f"send_{idx}"):
                send_resume_email(
                    to_email=custom_email,
                    subject=subject,
                    body=email_body,
                    resume_path="temp_resume.pdf"
                )
                st.success("✅ Resume sent successfully!")
