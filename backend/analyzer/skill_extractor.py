import spacy
import re
from spacy.matcher import PhraseMatcher
import json
import os

nlp = spacy.load("en_core_web_sm")


BASE_DIR = os.path.dirname(__file__)
skills_file = os.path.join(BASE_DIR, "skills.json")

with open(skills_file, "r") as f:
    SKILLS_DB = json.load(f)

def normalize_text(text):
    text = text.lower()

    # Standardize separators
    text = re.sub(r"[|•·]", " ", text)
    text = re.sub(r"[()/]", " ", text)

    replacements = {
        r"\bnodejs\b": "node.js",
        r"\bnode js\b": "node.js",
        r"\bci cd\b": "ci/cd",
        r"\bci-cd\b": "ci/cd",
        r"\bpostgres\b": "postgresql",
        r"\bjs\b": "javascript",
        r"\bts\b": "typescript",
        r"\bpy\b": "python",
        r"\breactjs\b": "react",
        r"\bnextjs\b": "next.js",
        r"\bvuejs\b": "vue",
        r"\basp net\b": "asp.net",
        r"\bdot net\b": ".net",
        r"\bgcp\b": "google cloud platform",
        r"\baws cloud\b": "aws",
        r"\bml\b": "machine learning",
        r"\bdl\b": "deep learning",
        r"\bnlp\b": "natural language processing",
        r"\bai\b": "artificial intelligence",
        r"\brestful\b": "rest api",
        r"\brest api\b": "rest api",
        r"\boops\b": "oop",
        r"\bobject oriented programming\b": "oop"
    }

    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text

def extract_skills(text):
    text_lower = normalize_text(text)
    doc = nlp(text_lower)

    categorized_skills = {}

    matcher = PhraseMatcher(nlp.vocab)

    for category, skills in SKILLS_DB.items():
        patterns = [nlp.make_doc(skill) for skill in skills]
        matcher.add(category, patterns)

    matches = matcher(doc)

    found_skills = {}

    for match_id, start, end in matches:
        category = nlp.vocab.strings[match_id]
        skill = doc[start:end].text

        if category not in found_skills:
            found_skills[category] = set()

        found_skills[category].add(skill)

    for category, skills in found_skills.items():
        categorized_skills[category] = sorted(list(skills))

    return categorized_skills

