from resume_reader.resume_reader import extract_resume_text
import re


COMMON_SKILLS = [
    "construction management",
    "project management",
    "site management",
    "civil engineering",
    "architecture",
    "architectural design",
    "structural engineering",
    "quantity surveying",
    "cost estimation",
    "budgeting",
    "planning",
    "contracts",
    "health and safety",
    "risk management",
    "autocad",
    "revit",
    "bim",
    "blueprints",
    "building regulations"
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
