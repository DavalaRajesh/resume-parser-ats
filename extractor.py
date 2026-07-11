import re
import spacy

nlp = spacy.load("en_core_web_sm")
SKILLS = [
    "Python",
    "Java",
    "C",
    "C++",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Node.js",
    "Flask",
    "Django",
    "Bootstrap",
    "Tailwind CSS",
    "Git",
    "GitHub",
    "SQL",
    "PostgreSQL",
    "MySQL",
    "MongoDB",
    "Docker",
    "AWS",
    "Firebase"
]
SKILL_ALIASES = {
    "js": "JavaScript",
    "javascript": "JavaScript",
    "reactjs": "React",
    "react.js": "React",
    "nodejs": "Node.js",
    "node.js": "Node.js",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "py": "Python",
    "html5": "HTML",
    "css3": "CSS",
    "c sharp": "C#"
}

def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0) if match else None


def extract_phone(text):
    match = re.search(r'(\+?\d[\d\s-]{8,15}\d)', text)
    return match.group(0) if match else None


def extract_name(text):

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    blacklist = [
        "frontend", "developer", "engineer", "student",
        "python", "java", "html", "css", "javascript",
        "react", "flask"
    ]

    for line in lines[:10]:

        if len(line.split()) >= 2:

            lower = line.lower()

            if not any(word in lower for word in blacklist):
                return line

    doc = nlp(text)

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            if len(ent.text.split()) >= 2:
                return ent.text

    return None

import re

def extract_skills(text):

    found = set()
    text_lower = text.lower()

    for skill in SKILLS:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text_lower):
            found.add(skill)

    for alias, standard in SKILL_ALIASES.items():
        pattern = r"\b" + re.escape(alias) + r"\b"

        if re.search(pattern, text_lower):
            found.add(standard)

    return sorted(found)

import re

def extract_education(text):

    education = {
        "degree": None,
        "institution": None,
        "year": None
    }

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    degree_patterns = [
        r"B\.?\s?Tech",
        r"B\.?\s?E",
        r"M\.?\s?Tech",
        r"MCA",
        r"MBA",
        r"B\.?\s?Sc",
        r"M\.?\s?Sc",
        r"Diploma"
    ]

    for line in lines:

        # Degree
        for pattern in degree_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                education["degree"] = line

        # Institution
        if "college" in line.lower() or "university" in line.lower():
            education["institution"] = line

        # Year (example: 2023-2027)
        year = re.search(r"(20\d{2})\s*[-–]\s*(20\d{2})", line)
        if year:
            education["year"] = year.group(2)

    return education
def extract_resume_data(text):

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "education": extract_education(text),
        "skills": extract_skills(text)
    }