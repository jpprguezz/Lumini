from django import forms
from django.contrib.auth.models import User
from .models import Profile

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Escribe algo sobre ti...'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }