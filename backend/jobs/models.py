from django.db import models

class JobDescription(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    extracted_skills = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title