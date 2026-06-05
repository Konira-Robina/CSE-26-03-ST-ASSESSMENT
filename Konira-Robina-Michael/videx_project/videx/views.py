from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Video
from .forms import VideoUploadForm

# Create your views here.


def landing(request):
    if request.session.get('username'):
        return redirect('dashboard')
    return render(request, 'videos/landing.html')


def join(request):
    if request.session.get('username'):
        return redirect('dashboard')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        if not username:
            error = 'Please enter a username.'
        elif len(username) < 2:
            error = 'Username must be at least 2 characters.'
        else:
            request.session['username'] = username
            request.session.set_expiry(0)  # expires when browser closes
            return redirect('dashboard')

    return render(request, 'videos/join.html', {'error': error})


def dashboard(request):
    if not request.session.get('username'):
        return redirect('landing')
    videos = Video.objects.filter(username=request.session['username']).order_by('-uploaded_at')
    return render(request, 'videos/dashboard.html', {
        'videos': videos,
        'username': request.session['username']
    })


def upload_video(request):
    if not request.session.get('username'):
        return redirect('landing')

    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.username = request.session['username']
            video.save()
            return JsonResponse({'success': True, 'message': 'Video uploaded successfully!'})
        else:
            errors = {field: list(errs) for field, errs in form.errors.items()}
            return JsonResponse({'success': False, 'errors': errors}, status=400)

    form = VideoUploadForm()
    return render(request, 'videos/upload.html', {'form': form})


def watch_video(request, pk):
    if not request.session.get('username'):
        return redirect('landing')
    video = get_object_or_404(Video, pk=pk, username=request.session['username'])
    video.views += 1
    video.save(update_fields=['views'])
    return render(request, 'videos/watch.html', {'video': video})
