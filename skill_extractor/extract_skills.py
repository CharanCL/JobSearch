from resume_reader.resume_reader import extract_resume_text
import re

COMMON_SKILLS = [
    "business analysis",
    "market research",
    "strategy",
    "operations",
    "project management",
    "finance",
    "financial modeling",
    "marketing",
    "digital marketing",
    "sales",
    "customer acquisition",
    "stakeholder management",
    "leadership",
    "team management",
    "process improvement",
    "supply chain",
    "data analysis",
    "excel",
    "power bi",
    "tableau"
]


def extract_skills(resume_text):
    resume_text = resume_text.lower()
    found_skills = []

    for skill in COMMON_SKILLS:
        if re.search(r"\b" + re.escape(skill) + r"\b", resume_text):
            found_skills.append(skill)

    return list(set(found_skills))


if __name__ == "__main__":
    from resume_reader.resume_reader import extract_resume_text

    text = extract_resume_text(
        r"C:\GITHUB\JobSearch\resume.pdf"
    )

    skills = extract_skills(text)
    print("✅ Extracted Skills:")
    for skill in skills:
        print("-", skill)
