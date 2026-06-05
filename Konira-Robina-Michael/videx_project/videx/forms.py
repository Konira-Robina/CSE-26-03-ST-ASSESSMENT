from django import forms
from .models import Video


class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'quality', 'date_of_publishing', 'video_file', 'thumbnail']
        widgets = {
            'date_of_publishing': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 6}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise forms.ValidationError('Required field')
        return title

    def clean_quality(self):
        quality = self.cleaned_data.get('quality', '').strip()
        if not quality:
            raise forms.ValidationError('Required field')
        return quality

    def clean_date_of_publishing(self):
        date = self.cleaned_data.get('date_of_publishing')
        if not date:
            raise forms.ValidationError('Required field')
        return date

    def clean_video_file(self):
        video = self.cleaned_data.get('video_file')
        if not video:
            raise forms.ValidationError('Required field')
        return video

    def clean_thumbnail(self):
        thumb = self.cleaned_data.get('thumbnail')
        if not thumb:
            raise forms.ValidationError('Required field')
        return thumb
