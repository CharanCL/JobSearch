
import streamlit as st

from resume_reader.resume_reader import extract_resume_text
from skill_extractor.extract_skills import extract_skills
from job_search.live_jobs import fetch_jobs_live

from ai_matcher.matcher import rank_jobs
from email_agent.send_email import send_resume_email
from email_agent.email_body import generate_email_body


st.set_page_config(page_title="AI Job Application Assistant", layout="wide")

st.title("🤖 AI Job Application Assistant")
st.write("Search jobs, review matches, preview emails, and send your resume safely.")

# Sidebar
st.sidebar.header("Settings")
location = st.sidebar.text_input("Job Location", value="London")
hr_email = st.sidebar.text_input("HR Email", value="hr@example.com")
resume_path = r"C:\GITHUB\JobSearch\resume.pdf"

# Load resume
resume_text = extract_resume_text(resume_path)
skills = extract_skills(resume_text)

st.sidebar.subheader("Extracted Skills")
st.sidebar.write(", ".join(skills))

# Fetch jobs
if st.button("🔍 Find Matching Jobs"):
    with st.spinner("Searching jobs..."):
        jobs = fetch_jobs_live(skills, location)
        results = rank_jobs(resume_text, jobs)
        st.session_state["results"] = results

# Show results
if "results" in st.session_state:
    st.subheader("🏆 Job Matches")

    for idx, job in enumerate(st.session_state["results"], start=1):
        with st.expander(f"{idx}. {job['title']} @ {job['company']}"):
            st.write(f"**Match Score:** {job['score']}%")
            st.write(f"**Matched Skills:** {', '.join(job['matched_skills'])}")

            subject = f"Application for {job['title']}"
            email_body = generate_email_body(job["title"], job["company"])

            st.subheader("📨 Email Preview")
            st.text_area("Email Body", email_body, height=220)

            if st.button(f"✅ Send Resume to {job['company']}", key=f"send_{idx}"):
                send_resume_email(
                    to_email=hr_email,
                    subject=subject,
                    body=email_body,
                    resume_path=resume_path
                )
                st.success("✅ Resume sent successfully!")
