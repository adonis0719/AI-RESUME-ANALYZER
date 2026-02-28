from django.shortcuts import render
from resumes.models import Resume
from jobs.models import JobDescription
from .matcher import calculate_match
from django.contrib.auth.decorators import login_required

@login_required
def compare(request):
    resumes = Resume.objects.filter(user=request.user)
    jobs = JobDescription.objects.filter(user=request.user)    
    result = None

    if request.method == 'POST':
        resume_id = request.POST.get('resume_id')
        job_id = request.POST.get('job_id')

        resume = Resume.objects.get(id=resume_id)
        job = JobDescription.objects.get(id=job_id)

        result = calculate_match(resume.skills or {}, job.extracted_skills or {})

    return render(request, 'compare.html', {
        'resumes': resumes,
        'jobs': jobs,
        'result': result
    })




from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def compare_api(request):
    resume_id = request.data.get('resume_id')
    job_id = request.data.get('job_id')

    resume = Resume.objects.get(id=resume_id, user=request.user)
    job = JobDescription.objects.get(id=job_id, user=request.user)

    result = calculate_match(resume.skills or {}, job.extracted_skills or {})

    return Response(result)