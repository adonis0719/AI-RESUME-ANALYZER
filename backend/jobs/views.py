from django.shortcuts import render, redirect
from .forms import JobForm
from analyzer.skill_extractor import extract_skills
from django.contrib.auth.decorators import login_required

@login_required
def upload_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user
            job.save()            

            skills = extract_skills(job.description)
            job.extracted_skills = skills
            job.save()

            return redirect('home')
    else:
        form = JobForm()

    return render(request, 'job_upload.html', {'form': form})