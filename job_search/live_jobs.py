
import os
import requests

SERPAPI_KEY = os.getenv("SERPAPI_KEY")


def fetch_jobs_live(skills, location="London"):
    if not SERPAPI_KEY:
        raise RuntimeError("SerpAPI key not set")

    # Google Jobs query – works VERY well for UK construction & architecture
    query = "construction manager OR site manager OR architect OR civil engineer"

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
            "description": job.get("description", "")
        })

    print(f"SerpAPI returned {len(jobs)} jobs")

    
	return [
    {
        "title": job.get("title", ""),
        "company": job.get("company_name", ""),
        "description": job.get("description", ""),
        "posted_at": job.get("published_at") or job.get("posted_at")
    }
    for job in all_jobs[:max_jobs]
	]

