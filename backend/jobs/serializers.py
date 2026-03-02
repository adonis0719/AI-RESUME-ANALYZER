from .models import JobDescription
from rest_framework import serializers
from analyzer.skill_extractor import extract_skills

class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobDescription
        fields = '__all__'
        read_only_fields = ['user', 'extracted_skills']

    def create(self, validated_data):
        job = JobDescription.objects.create(**validated_data)

        job.extracted_skills = extract_skills(job.description)
        job.save()

        return job