from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Job, Resume


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class RoleSelectionForm(forms.Form):
    ROLE_CHOICES = [
        ('candidate', 'Candidate'),
        ('recruiter', 'Recruiter'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)


class CandidateRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class RecruiterRegistrationForm(UserCreationForm):
    company_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'company_name', 'email', 'password1', 'password2']


class JobSearchForm(forms.Form):
    keyword = forms.CharField(max_length=100, required=False)
    location = forms.CharField(max_length=100, required=False)


class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['file']


class JobPostForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'salary']
