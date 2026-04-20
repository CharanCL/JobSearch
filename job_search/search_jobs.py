
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

def search_jobs():
    url = "https://in.indeed.com/jobs?q=python+sql+git&l=Bangalore"
    print(f"🔍 Searching jobs: {url}")

    response = requests.get(url, headers=HEADERS)
    print("HTML length:", len(response.text))
    soup = BeautifulSoup(response.text, "html.parser")

    job_cards = soup.select("a.tapItem")

    jobs = []
    for card in job_cards[:5]:
        title = card.select_one("h2 span")
        company = card.select_one(".companyName")
        location = card.select_one(".companyLocation")

        jobs.append({
            "title": title.text.strip() if title else "N/A",
            "company": company.text.strip() if company else "N/A",
            "location": location.text.strip() if location else "N/A",
        })

    return jobs


if __name__ == "__main__":
    jobs = search_jobs()
    print("Found jobs:")
    for job in jobs:
        print(job)


