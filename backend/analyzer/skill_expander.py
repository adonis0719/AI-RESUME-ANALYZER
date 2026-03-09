"""
Skill Expansion using AI Embeddings.
Expands extracted skills using semantic similarity (e.g. rest api ≈ backend development).
"""

import os
import json

BASE_DIR = os.path.dirname(__file__)
SKILLS_FILE = os.path.join(BASE_DIR, "skills.json")

SIMILARITY_THRESHOLD = 0.75

_model = None
_skill_embeddings = None
_all_skills_flat = None


def _load_skills_flat():
    """Load all skills from skills.json as flat list with category."""
    global _all_skills_flat
    if _all_skills_flat is not None:
        return _all_skills_flat
    try:
        with open(SKILLS_FILE, "r") as f:
            data = json.load(f)
        flat = []
        for category, skills in data.items():
            for s in skills:
                if s and isinstance(s, str):
                    flat.append((s.lower(), category))
        _all_skills_flat = flat
        return flat
    except Exception:
        return []


def _get_model():
    """Lazy load SentenceTransformer model."""
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            _model = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception:
            pass
    return _model


def _get_skill_embeddings():
    """Lazy load embeddings for all skills in skills.json."""
    global _skill_embeddings
    if _skill_embeddings is not None:
        return _skill_embeddings
    model = _get_model()
    if model is None:
        return None
    try:
        skills_flat = _load_skills_flat()
        if not skills_flat:
            return None
        texts = [t[0] for t in skills_flat]
        _skill_embeddings = (model.encode(texts), skills_flat)
        return _skill_embeddings
    except Exception:
        return None


def expand_skills(extracted_skills):
    """
    Expand extracted skills using semantic similarity.
    Adds similar skills from skills.json above SIMILARITY_THRESHOLD.

    Args:
        extracted_skills: dict of category -> list of skills (from skill extractor)

    Returns:
        dict: Same structure as extracted_skills but with added similar skills per category.
    """
    if not extracted_skills or not isinstance(extracted_skills, dict):
        return extracted_skills or {}

    emb_data = _get_skill_embeddings()
    if emb_data is None:
        return extracted_skills

    try:
        from sklearn.metrics.pairwise import cosine_similarity
    except ImportError:
        return extracted_skills

    db_embeddings, db_skills = emb_data
    model = _get_model()
    if model is None:
        return extracted_skills

    result = {}
    for category, skills in extracted_skills.items():
        skill_list = list(skills) if isinstance(skills, (list, set)) else []
        existing = set(s.lower() for s in skill_list if s)

        if not skill_list:
            result[category] = skill_list
            continue

        # Embed extracted skills for this category
        try:
            ext_emb = model.encode([s for s in skill_list if s])
        except Exception:
            result[category] = skill_list
            continue

        # Find similar skills from DB
        sim = cosine_similarity(ext_emb, db_embeddings)
        for i in range(sim.shape[0]):
            for j in range(sim.shape[1]):
                if sim[i][j] >= SIMILARITY_THRESHOLD:
                    skill_name, skill_cat = db_skills[j]
                    if skill_name not in existing and skill_cat == category:
                        existing.add(skill_name)
                        skill_list.append(skill_name)

        result[category] = sorted(list(set(skill_list)))

    return result
