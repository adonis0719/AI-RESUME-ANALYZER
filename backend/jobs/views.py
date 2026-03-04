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





from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import JobSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import JobDescription

from rest_framework import status

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def job_list_api(request):

    if request.method == 'GET':
        jobs = JobDescription.objects.filter(user=request.user)
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_job_api(request, job_id):

    try:
        job = JobDescription.objects.get(id=job_id, user=request.user)
        job.delete()
        return Response({"message": "Job deleted"}, status=status.HTTP_200_OK)

    except JobDescription.DoesNotExist:
        return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)    