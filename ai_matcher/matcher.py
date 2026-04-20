
import re
from job_search.mock_jobs import get_mock_jobs




SKILL_SYNONYMS = {
    "construction": {
        "construction", "site", "site management", "building"
    },
    "management": {
        "management", "project management", "planning", "coordination"
    },
    "architecture": {
        "architecture", "architectural", "design", "architect"
    },
    "engineering": {
        "civil", "structural", "engineering"
    },
    "costing": {
        "cost", "costing", "budgeting", "estimation", "quantity surveying"
    },
    "software": {
        "autocad", "revit", "bim"
    },
    "contracts": {
        "contracts", "procurement", "tender", "compliance"
    },
    "safety": {
        "health", "safety", "hse", "risk"
    }
}




def tokenize(text):
    text = text.lower()
    words = re.findall(r"[a-z0-9]+", text)

    normalized = set(words)

    for base, variants in SKILL_SYNONYMS.items():
        if any(v in words for v in variants):
            normalized.add(base)

    return normalized



def match_score(resume_text, job_description):
    resume_tokens = tokenize(resume_text)
    job_tokens = tokenize(job_description)

    if not job_tokens:
        return 0, []

    common = resume_tokens & job_tokens

    score = (len(common) / len(job_tokens)) * 100
    return round(score, 2), list(common)




def rank_jobs(resume_text, jobs):
    ranked = []

    for job in jobs:
        score, matched = match_score(
            resume_text,
            job["description"]
        )

        ranked.append({
            "title": job["title"],
            "company": job["company"],
            "score": score,
            "matched_skills": matched
        })

    ranked.sort(key=lambda x: x["score"], reverse=True)
    return ranked
