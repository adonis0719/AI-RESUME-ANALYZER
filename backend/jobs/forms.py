from django import forms
from .models import JobDescription

class JobForm(forms.ModelForm):
    class Meta:
        model = JobDescription
        fields = ['title', 'description']