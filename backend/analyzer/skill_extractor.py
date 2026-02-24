import spacy
import re
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")

SKILLS_DB = {
    "programming_languages": [
        "python", "java", "c", "c++", "javascript"
    ],
    "frameworks": [
        "django", "flask", "angular", "react"
    ],
    "web_technologies": [
        "html", "html5", "css", "bootstrap", "jquery"
    ],
    "databases": [
        "mysql", "sql", "mongodb"
    ],
    "tools": [
        "git", "docker", "aws"
    ],
    "concepts": [
        "rest api", "machine learning", "data analysis",
        "agile", "microservices"
    ]
}

def extract_skills(text):
    text_lower = text.lower()
    doc = nlp(text_lower)

    categorized_skills = {}

    for category, skills in SKILLS_DB.items():
        matcher = PhraseMatcher(nlp.vocab)
        patterns = [nlp.make_doc(skill) for skill in skills]
        matcher.add(category, patterns)

        matches = matcher(doc)

        found = set()

        for match_id, start, end in matches:
            skill = doc[start:end].text
            found.add(skill)

        # Regex handling
        if "c++" in skills and re.search(r"\bc\+\+\b", text_lower):
            found.add("c++")

        if "rest api" in skills and re.search(r"\brest\b", text_lower):
            found.add("rest api")

        if found:
            categorized_skills[category] = sorted(list(found))

    return categorized_skills