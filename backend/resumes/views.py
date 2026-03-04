from django.shortcuts import render, redirect
from .forms import ResumeUploadForm
from .models import Resume
import pdfplumber
import docx
from analyzer.skill_extractor import extract_skills
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')

@login_required
def upload_resume(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()            

            # Extract text
            file_path = resume.file.path

            extracted_text = ""

            if file_path.endswith('.pdf'):
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        extracted_text += page.extract_text() or ""

            elif file_path.endswith('.docx'):
                doc = docx.Document(file_path)
                for para in doc.paragraphs:
                    extracted_text += para.text + "\n"

            resume.extracted_text = extracted_text
            skills = extract_skills(extracted_text)
            resume.skills = skills
            resume.save()

            return redirect('home')
    else:
        form = ResumeUploadForm()

    return render(request, 'upload.html', {'form': form})


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ResumeSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from rest_framework import status

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def resume_list_api(request):

    if request.method == 'GET':
        resumes = Resume.objects.filter(user=request.user)
        serializer = ResumeSerializer(resumes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ResumeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_resume_api(request, resume_id):

    try:
        resume = Resume.objects.get(id=resume_id, user=request.user)
        resume.delete()
        return Response({"message": "Resume deleted"}, status=status.HTTP_200_OK)

    except Resume.DoesNotExist:
        return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)    







