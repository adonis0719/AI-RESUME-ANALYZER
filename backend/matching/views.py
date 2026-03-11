from django.shortcuts import render
from resumes.models import Resume
from jobs.models import JobDescription
from .matcher import calculate_match, calculate_hybrid_match
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .question_generator import generate_interview_questions


@login_required
def compare(request):
    resumes = Resume.objects.filter(user=request.user)
    jobs = JobDescription.objects.filter(user=request.user)
    result = None

    if request.method == 'POST':
        resume_id = request.POST.get('resume_id')
        job_id = request.POST.get('job_id')

        resume = Resume.objects.get(id=resume_id, user=request.user)
        job = JobDescription.objects.get(id=job_id, user=request.user)

        result = calculate_match(resume.skills or {}, job.extracted_skills or {})

    return render(request, 'compare.html', {
        'resumes': resumes,
        'jobs': jobs,
        'result': result
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def compare_api(request):
    resume_id = request.data.get('resume_id')
    job_id = request.data.get('job_id')

    resume = Resume.objects.get(id=resume_id, user=request.user)
    job = JobDescription.objects.get(id=job_id, user=request.user)

    result = calculate_hybrid_match(
        resume.skills or {},
        job.extracted_skills or {},
        resume_text=resume.extracted_text,
        job_text=job.description,
    )

    # Interview questions must be inside the function
    questions = generate_interview_questions(result.get("recommendations", []))
    result["interview_questions"] = questions

    return Response(result)