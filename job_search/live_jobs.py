import requests
import os

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
def fetch_jobs_live(skills, location="London", max_jobs=30):
    if not SERPAPI_KEY:
        raise RuntimeError("SerpAPI key not set")

    queries = build_queries(skills, location)

    all_jobs = []
    seen = set()

    for query in queries:
        # Pagination (2 pages per query)
        for start in [0, 10]:

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
                title = job.get("title", "").strip().lower()
                company = job.get("company_name", "").strip().lower()

                key = (title, company)

                if key in seen:
                    continue

                seen.add(key)

                all_jobs.append({
                    "title": job.get("title", ""),
                    "company": job.get("company_name", ""),
                    "location": job.get("location", ""),
                    "via": job.get("via", ""),
                    "description": job.get("description", ""),
                    "posted_at": job.get("published_at") or job.get("posted_at"),
                    "role": classify_role(job.get("title", "")),
                    "query_used": query
                })

                # ✅ Stop early if enough jobs collected
                if len(all_jobs) >= max_jobs:
                    print(f"Collected {len(all_jobs)} jobs (early stop)")
                    return all_jobs

    print(f"Total unique jobs fetched: {len(all_jobs)}")
    return all_jobs[:max_jobs]
