from django.contrib import admin
from django.contrib import admin
from .models import Video

# Register your models here.


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'quality', 'views', 'uploaded_at']
    list_filter = ['quality']
    search_fields = ['title', 'user__username'] 
    
