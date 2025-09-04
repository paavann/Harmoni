from django.db import models
from django.conf import settings
from django.utils import timezone



class Journal(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='journals'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.email})"
    

    class Meta:
        ordering = ['-created_at']



class JournalEntry(models.Model):
    journal = models.ForeignKey(
        Journal,
        on_delete=models.CASCADE,
        related_name='entries'
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=100, blank=True, null=True)
    ai_response = models.TextField(blank=True, null=True)
    sentiment = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_editable(self):
        return self.created_at.date() == timezone.now().date() 

    def __str__(self):
        return f"{self.title} ({self.journal.name})"

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['journal', '-created_at']),
        ]