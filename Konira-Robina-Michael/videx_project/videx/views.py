from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Video
from .forms import JoinForm, VideoUploadForm


def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')


def join(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = JoinForm()
    if request.method == 'POST':
        form = JoinForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    return render(request, 'join.html', {'form': form})


@login_required
def dashboard(request):
    videos = Video.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'dashboard.html', {'videos': videos})


@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.save()
            return JsonResponse({'success': True, 'message': 'Video uploaded successfully!'})
        else:
            errors = {field: list(errs) for field, errs in form.errors.items()}
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    form = VideoUploadForm()
    return render(request, 'upload.html', {'form': form})


@login_required
def watch_video(request, pk):
    video = get_object_or_404(Video, pk=pk, user=request.user)
    video.views += 1
    video.save(update_fields=['views'])
    return render(request, 'watch.html', {'video': video})
