from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from accounts.models import Apply


class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Apply

        fields = [
            'full_name',
            'email',
            'phone',
            'resume_file',
            'cover_letter_file',
        ]

        widgets = {
            'full_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your full name'
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your email'
                }
            ),

            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your phone number'
                }
            ),

            'resume_file': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'cover_letter_file': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 7,
                    'placeholder': 'Write your cover letter'
                }
            ),
        }
