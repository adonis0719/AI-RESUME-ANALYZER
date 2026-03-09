from django.db import models
from django.contrib.auth.models import User


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="resumes/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    extracted_text = models.TextField(blank=True, null=True)
    skills = models.JSONField(blank=True, null=True)
    candidate_email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.title
