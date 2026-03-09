WEIGHTS = {
    "programming_languages": 30,
    "frameworks": 25,
    "databases": 15,
    "web_technologies": 10,
    "tools": 10,
    "concepts": 10
}


def _load_domain_weights(domain):
    """Load weights for a domain from domain_weights.json. Returns None on failure."""
    try:
        import os
        import json
        path = os.path.join(os.path.dirname(__file__), "..", "analyzer", "domain_weights.json")
        with open(path, "r") as f:
            data = json.load(f)
        return data.get(domain)
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


def calculate_hybrid_match(resume_skills, job_skills, resume_text=None, job_text=None):
    """
    Hybrid matcher: domain detection + domain weights + rule score + AI semantic score.
    Falls back to rule-based only if AI modules fail.
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

    expanded_resume_skills = resume_skills
    try:
        expanded_resume_skills = expand_skills(dict(resume_skills))
    except Exception:
        pass

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
    rule_result = calculate_match(resume_skills, job_skills)
    rule_result["domain"] = "IT"
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
