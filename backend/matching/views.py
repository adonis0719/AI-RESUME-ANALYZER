from django.shortcuts import render
from resumes.models import Resume
from jobs.models import JobDescription
from .matcher import calculate_match

def compare(request):
    resumes = Resume.objects.all()
    jobs = JobDescription.objects.all()

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