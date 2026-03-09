import os
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from analyzer.pdf_extractor import extract_text_from_pdf, extract_email
from analyzer.skill_extractor import extract_skills
from matching.matcher import calculate_hybrid_match


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def bulk_analyze(request):
    job_description = request.data.get("job_description")

    resumes = request.FILES.getlist("resumes")

    job_skills = extract_skills(job_description)

    results = []

    temp_folder = os.path.join(settings.MEDIA_ROOT, "temp_recruiter")

    os.makedirs(temp_folder, exist_ok=True)

    for file in resumes:
        file_path = os.path.join(temp_folder, file.name)

        with open(file_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        text = extract_text_from_pdf(file_path)

        resume_skills = extract_skills(text)

        match = calculate_hybrid_match(
            resume_skills,
            job_skills,
            resume_text=text,
            job_text=job_description,
        )

        score = match["overall_match_percentage"]

        email = extract_email(text)

        results.append(
            {
                "name": file.name,
                "score": score,
                "file_url": f"/media/temp_recruiter/{file.name}",
                "details": match,
                "email": email,
            }
        )

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return Response({"ranked_resumes": results})
