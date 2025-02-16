# models.py
from django.db import models

class Resume(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class ResumeFeedback(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    prediction = models.CharField(max_length=255)
    correct = models.BooleanField(default=False)
    feedback_text = models.TextField(null=True, blank=True)  # Optional field for additional feedback
