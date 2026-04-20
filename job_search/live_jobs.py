
import os
import requests

SERPAPI_KEY = os.getenv("SERPAPI_KEY")


def fetch_jobs_live(skills, location="London", max_jobs=30):
    if not SERPAPI_KEY:
        raise RuntimeError("SerpAPI key not set")

    query = (
        "construction manager OR site manager "
        "OR architect OR civil engineer"
    )

    params = {
        "engine": "google_jobs",
        "q": query,
        "location": location,
        "hl": "en",
        "api_key": SERPAPI_KEY
    }

    response = requests.get("https://serpapi.com/search", params=params)
    response.raise_for_status()
    data = response.json()

    jobs = []

    for job in data.get("jobs_results", []):
        jobs.append({
            "title": job.get("title", ""),
            "company": job.get("company_name", ""),
            "description": job.get("description", ""),
            "posted_at": job.get("published_at") or job.get("posted_at")
        })

    print(f"SerpAPI returned {len(jobs)} jobs")
    return jobs[:max_jobs]
