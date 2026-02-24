from django.db import models

class Resume(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    extracted_text = models.TextField(blank=True, null=True)
    skills = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.title