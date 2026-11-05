from django import forms
from .models import ShootingSession

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = ShootingSession
        fields = ['title', 'session_type', 'video', 'notes']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Free Throw Practice - Feb 3, 2026'
            }),
            'session_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'video': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'video/*'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add any notes about this session (optional)'
            }),
        }
        
    def clean_video(self):
        video = self.cleaned_data.get('video')
        if video:
            # Check file size (100MB limit)
            if video.size > 100 * 1024 * 1024:
                raise forms.ValidationError('Video file size must be less than 100MB')
            
            # Check file extension
            valid_extensions = ['.mp4', '.avi', '.mov', '.mkv']
            if not any(video.name.lower().endswith(ext) for ext in valid_extensions):
                raise forms.ValidationError('Please upload a valid video file (.mp4, .avi, .mov, .mkv)')
        
        return video
