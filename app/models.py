from django.db import models

class AudioFile(models.Model):
    audio = models.FileField(upload_to='audio/')
    transcript = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
