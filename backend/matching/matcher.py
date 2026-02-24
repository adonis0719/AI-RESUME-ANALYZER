def calculate_match(resume_skills, job_skills):
    result = {
        "category_match": {},
        "missing_skills": {},
        "overall_match_percentage": 0
    }

    total_categories = 0
    total_percentage = 0

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

        result["category_match"][category] = {
            "matched": list(matched),
            "missing": list(missing),
            "percentage": round(percentage, 2)
        }

        result["missing_skills"][category] = list(missing)

        total_categories += 1
        total_percentage += percentage

    if total_categories > 0:
        result["overall_match_percentage"] = round(total_percentage / total_categories, 2)

    return result   