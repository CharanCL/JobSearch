
from resume_reader.resume_reader import extract_resume_text
from skill_extractor.extract_skills import extract_skills
from job_search.live_jobs import fetch_jobs_live
from ai_matcher.matcher import rank_jobs

resume_text = extract_resume_text(
    r"C:\GITHUB\JobSearch\resume.pdf"
)

skills = extract_skills(resume_text)
location = "United Kingdom"

jobs = fetch_jobs_live(skills, location)
results = rank_jobs(resume_text, jobs)

print("\n🏆 UK Job Match Results:\n")
for job in results:
    print(f"{job['title']} @ {job['company']}")
    print(f"Match Score: {job['score']}%")
    print(f"Matched Skills: {job['matched_skills']}")
    print("-" * 40)
