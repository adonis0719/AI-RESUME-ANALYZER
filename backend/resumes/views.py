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