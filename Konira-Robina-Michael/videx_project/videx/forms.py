from django import forms
from django.contrib.auth.models import User
from .models import Video


class JoinForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=6)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('confirm_password')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


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
