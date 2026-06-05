from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Video
from .forms import VideoUploadForm

# Create your views here.


def landing(request):
    if request.session.get('username'):
        return redirect('dashboard')
    return render(request, 'landing.html')


def dashboard(request):
    videos = Video.objects.all().order_by('-uploaded_at')
    return render(request, 'dashboard.html', {'videos': videos})

def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            return JsonResponse({'success': True, 'message': 'Video uploaded successfully!'})
        else:
            errors = {field: list(errs) for field, errs in form.errors.items()}
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    form = VideoUploadForm()
    return render(request, 'upload.html', {'form': form})


def watch_video(request, pk):
    video = get_object_or_404(Video, pk=pk)
    video.views += 1
    video.save(update_fields=['views'])
    return render(request, 'watch.html', {'video': video})
