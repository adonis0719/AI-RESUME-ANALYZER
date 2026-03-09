from rest_framework import serializers
from .models import Resume
from analyzer.pdf_extractor import extract_text_from_pdf, extract_email
from analyzer.skill_extractor import extract_skills


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = "__all__"
        read_only_fields = ["user", "extracted_text", "skills"]

    def create(self, validated_data):
        resume = Resume.objects.create(**validated_data)

        text = extract_text_from_pdf(resume.file.path)
        resume.extracted_text = text

        email = extract_email(text)
        resume.candidate_email = email

        resume.skills = extract_skills(text)
        resume.save()

        return resume
