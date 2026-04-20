
from resume_reader.resume_reader import extract_resume_text
from job_search.mock_jobs import get_mock_jobs
from ai_matcher.matcher import rank_jobs
from job_search.live_jobs import fetch_jobs_live

resume_text = extract_resume_text(
    r"C:\GITHUB\JobSearch\resume.pdf"
)

jobs = get_mock_jobs()
results = rank_jobs(resume_text, jobs)

print("\n🏆 Job Match Results:\n")
for job in results:
    print(f"{job['title']} @ {job['company']}")
    print(f"Match Score: {job['score']}%")
    print(f"Matched Skills: {job['matched_skills']}")
    print("-" * 40)
