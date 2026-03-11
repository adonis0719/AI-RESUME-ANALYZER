import os
import json

WEIGHTS = {
    "programming_languages": 30,
    "backend_frameworks": 25,
    "databases_sql": 15,
    "frontend_frameworks_libraries": 10,
    "cloud_platforms": 10,
    "devops_tools": 10,
}

_DOMAIN_WEIGHTS_CACHE = None


def _load_domain_weights(domain):
    """Load weights for a domain from domain_weights.json. Cached. Returns None on failure."""
    global _DOMAIN_WEIGHTS_CACHE
    try:
        if _DOMAIN_WEIGHTS_CACHE is None:
            path = os.path.join(os.path.dirname(__file__), "..", "analyzer", "domain_weights.json")
            with open(path, "r") as f:
                _DOMAIN_WEIGHTS_CACHE = json.load(f)
        return _DOMAIN_WEIGHTS_CACHE.get(domain)
    except Exception:
        return None


def generate_recommendations(category_match):
    recommendations = []

    for category, data in category_match.items():
        for skill in data["missing"]:
            recommendations.append({
                "skill": skill,
                "category": category,
                "priority": data["weight"]  # higher weight = higher priority
            })

    # Sort by priority descending
    recommendations = sorted(recommendations, key=lambda x: x["priority"], reverse=True)

    return recommendations



def calculate_match(resume_skills, job_skills, weights=None):
    """
    Rule-based skill matching.
    weights: optional dict of category -> weight. If None, uses default WEIGHTS.
    """
    use_weights = weights if weights else WEIGHTS

    result = {
        "category_match": {},
        "overall_match_percentage": 0
    }

    weighted_score = 0
    total_weight = 0

    for category, job_skill_list in job_skills.items():
        resume_skill_list = resume_skills.get(category, [])

        job_set = set(job_skill_list)
        resume_set = set(resume_skill_list)

        matched = job_set.intersection(resume_set)
        missing = job_set.difference(resume_set)

        if job_set:
            percentage = (len(matched) / len(job_set)) * 100
        else:
            percentage = 0

        weight = use_weights.get(category, 0)

        weighted_score += ((percentage/100) * weight)
        total_weight += weight

        result["category_match"][category] = {
            "matched": list(matched),
            "missing": list(missing),
            "percentage": round(percentage, 2),
            "weight": weight
        }

    if total_weight > 0:
        result["overall_match_percentage"] = round((weighted_score / total_weight)*100, 2)

    result["recommendations"] = generate_recommendations(result["category_match"])

    return result


def _filter_skills_by_domain(skills, allowed_categories):
    """Keep only categories that belong to the detected domain. Prevents irrelevant categories (e.g. petroleum, real_estate) from appearing in IT job results."""
    if not allowed_categories:
        return skills
    return {k: v for k, v in skills.items() if k in allowed_categories}


def calculate_hybrid_match(resume_skills, job_skills, resume_text=None, job_text=None):
    """
    Hybrid matcher: domain detection + domain weights + rule score + AI semantic score.
    Only processes categories relevant to the detected domain - prevents css->petroleum,
    feasibility analysis->real_estate type misclassifications from appearing.
    """
    try:
        from analyzer.domain_detector import detect_domain
        from analyzer.ai_matcher import semantic_similarity
        from analyzer.skill_expander import expand_skills
    except ImportError:
        return _hybrid_fallback(resume_skills, job_skills)

    domain = detect_domain(job_skills)
    domain_weights = _load_domain_weights(domain)
    weights = domain_weights if domain_weights else WEIGHTS
    allowed_categories = set(weights.keys()) if weights else set(WEIGHTS.keys())

    job_skills = _filter_skills_by_domain(job_skills, allowed_categories)
    resume_skills = _filter_skills_by_domain(resume_skills, allowed_categories)

    try:
        expanded = expand_skills(dict(resume_skills))
        expanded_resume_skills = _filter_skills_by_domain(expanded, allowed_categories)
    except Exception:
        expanded_resume_skills = resume_skills

    rule_result = calculate_match(expanded_resume_skills, job_skills, weights=weights)
    rule_score = rule_result["overall_match_percentage"]

    ai_score = None
    if resume_text is not None and job_text is not None:
        ai_score = semantic_similarity(resume_text, job_text)

    if ai_score is not None:

        hybrid_score = (rule_score * 0.6) + (ai_score * 0.4)

        # Never penalize perfect rule matches
        final_score = round(max(rule_score, hybrid_score), 2)

    else:
        final_score = rule_score

    result = dict(rule_result)
    result["domain"] = domain
    result["rule_score"] = rule_score
    result["ai_similarity"] = ai_score
    result["overall_match_percentage"] = final_score
    return result


def _hybrid_fallback(resume_skills, job_skills):
    """Fallback when AI modules unavailable - rule-based only."""
    domain_weights = _load_domain_weights("IT_SOFTWARE_DEVELOPMENT")
    weights = domain_weights if domain_weights else WEIGHTS
    allowed = set(weights.keys()) if weights else set(WEIGHTS.keys())
    job_skills = _filter_skills_by_domain(job_skills, allowed)
    resume_skills = _filter_skills_by_domain(resume_skills, allowed)
    rule_result = calculate_match(resume_skills, job_skills, weights=weights)
    rule_result["domain"] = "IT_SOFTWARE_DEVELOPMENT"
    rule_result["rule_score"] = rule_result["overall_match_percentage"]
    rule_result["ai_similarity"] = None
    return rule_result    


# CATEGORY_WEIGHTS = {
#     "programming_languages": 30,
#     "frameworks": 20,
#     "databases": 15,
#     "web_technologies": 10,
#     "devops_tools": 10,
#     "cloud_platform": 10,
#     "concepts": 5
# }


# def calculate_match(resume_skills, job_skills):

#     category_match = {}
#     recommendations = []

#     total_score = 0
#     total_weight = sum(CATEGORY_WEIGHTS.values())

#     for category, weight in CATEGORY_WEIGHTS.items():

#         job_list = set(job_skills.get(category, []))
#         resume_list = set(resume_skills.get(category, []))

#         if not job_list:
#             continue

#         matched = job_list.intersection(resume_list)
#         missing = job_list.difference(resume_list)

#         percentage = (len(matched) / len(job_list)) * 100

#         weighted_score = (percentage / 100) * weight
#         total_score += weighted_score

#         category_match[category] = {
#             "matched": list(matched),
#             "missing": list(missing),
#             "percentage": round(percentage, 2),
#             "weight": weight
#         }

#         for skill in missing:
#             recommendations.append({
#                 "skill": skill,
#                 "category": category,
#                 "priority": weight
#             })

#     overall_match = (total_score / total_weight) * 100

#     return {
#         "category_match": category_match,
#         "overall_match_percentage": round(overall_match, 2),
#         "recommendations": recommendations
#     }
