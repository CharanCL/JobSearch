import requests
import os
import hashlib
from job_search.applied_jobs import load_applied_jobs


def generate_job_id(title, company):
    key = f"{title}-{company}".lower().strip()
    return hashlib.md5(key.encode()).hexdigest()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")


# 🔹 Map skills → job roles
ROLE_MAP = {
    "construction": ["construction manager", "site manager", "project manager"],
    "architecture": ["architect", "project architect", "design manager"],
    "bim": ["bim coordinator", "bim manager"],
    "revit": ["bim coordinator"],
    "planning": ["planning engineer"],
    "autocad": ["design engineer", "draftsman"]
}


# 🔹 Build multiple queries dynamically
def build_queries(skills, location):
    roles = set()

    for skill in skills:
        skill = skill.lower()
        for key in ROLE_MAP:
            if key in skill:
                roles.update(ROLE_MAP[key])

    # fallback if nothing matched
    if not roles:
        roles = {"construction manager", "architect"}

    return [f"{role} jobs in {location}" for role in roles]


# 🔹 Classify job role from title
def classify_role(title):
    title = title.lower()

    if "bim" in title:
        return "BIM"
    elif "project manager" in title:
        return "Project Manager"
    elif "construction manager" in title:
        return "Construction Manager"
    elif "site engineer" in title or "site manager" in title:
        return "Site"
    elif "architect" in title:
        return "Architecture"
    elif "planning" in title:
        return "Planning"
    else:
        return "Other"


# 🔹 Main function
def fetch_jobs_live(skills, location="London", max_jobs=300):
    if not SERPAPI_KEY:
        raise RuntimeError("SerpAPI key not set")

    queries = build_queries(skills, location)

    all_jobs = []
    seen = set()
    applied_jobs = load_applied_jobs()  # ✅ load applied jobs

    for query in queries:
        for start in range(0, 50, 10):

            params = {
                "engine": "google_jobs",
                "q": query,
                "location": location,
                "hl": "en",
                "start": start,
                "api_key": SERPAPI_KEY
            }

            response = requests.get("https://serpapi.com/search", params=params)
            response.raise_for_status()
            data = response.json()

            for job in data.get("jobs_results", []):
                title_raw = job.get("title", "")
                company_raw = job.get("company_name", "")

                title = title_raw.strip().lower()
                company = company_raw.strip().lower()

                key = (title, company)

                if key in seen:
                    continue

                seen.add(key)

                # ✅ generate job_id
                job_id = generate_job_id(title_raw, company_raw)

                # ✅ skip if already applied
                if job_id in applied_jobs:
                    continue

                all_jobs.append({
                    "job_id": job_id,  # ✅ fixed comma
                    "title": title_raw,
                    "company": company_raw,
                    "location": job.get("location", ""),
                    "via": job.get("via", ""),
                    "description": job.get("description", ""),
                    "posted_at": job.get("published_at") or job.get("posted_at"),
                    "role": classify_role(title_raw),
                    "query_used": query
                })

                if len(all_jobs) >= max_jobs:
                    print(f"Collected {len(all_jobs)} jobs (early stop)")
                    return all_jobs

    print(f"Total unique jobs fetched: {len(all_jobs)}")
    return all_jobs[:max_jobs]