from django.db import models
from django.conf import settings
from django.utils import timezone



class Journal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='journals')
    title = models.CharField(max_length=255)
    # category = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField()

    ai_response = models.TextField(blank=True, null=True)
    sentiment = models.CharField(max_length=20, blank=True, null=True)

    # attachment = models.FileField(upload_to=journal_attachment_path, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_editable(self):
        return self.created_at.date() == timezone.now().date() 

    def __str__(self):
        return f"{self.title} ({self.user.email})"


    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]