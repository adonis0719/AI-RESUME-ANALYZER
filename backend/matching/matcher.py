WEIGHTS = {
    "programming_languages": 30,
    "frameworks": 25,
    "databases": 15,
    "web_technologies": 10,
    "tools": 10,
    "concepts": 10
}


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



def calculate_match(resume_skills, job_skills):
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

        weight = WEIGHTS.get(category, 0)

        weighted_score += (percentage * weight)
        total_weight += weight

        result["category_match"][category] = {
            "matched": list(matched),
            "missing": list(missing),
            "percentage": round(percentage, 2),
            "weight": weight
        }
        
    if total_weight > 0:
        result["overall_match_percentage"] = round(weighted_score / total_weight, 2)

    result["recommendations"] = generate_recommendations(result["category_match"])

    return result    
