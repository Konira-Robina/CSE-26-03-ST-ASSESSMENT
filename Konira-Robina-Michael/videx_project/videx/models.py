from django.db import models
from django.utils import timezone

# Create your models here.

class Video(models.Model):
    QUALITY_CHOICES = [
        ('360p', '360p'),
        ('720p', '720p'),
        ('1080p', '1080p'),
    ]

    username = models.CharField(max_length=150)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/')
    quality = models.CharField(max_length=10, choices=QUALITY_CHOICES)
    date_of_publishing = models.DateField()
    views = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title

    def formatted_views(self):
        if self.views >= 1_000_000:
            return f'{self.views / 1_000_000:.1f}M'
        elif self.views >= 1_000:
            return f'{self.views / 1_000:.0f}k'
        return str(self.views)

    def time_since(self):
        from django.utils.timesince import timesince
        return timesince(self.uploaded_at) + ' ago'
