from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Job, Resume, Application
# for resume validation check
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# defined for Resume validation check in JobApplicationForm class
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_FILE_TYPES = ['pdf', 'doc', 'docx']

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


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter', 'resume']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 5}),
        }

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            # Check file size
            if resume.size > MAX_FILE_SIZE:
                raise ValidationError(_('File size exceeds the maximum limit of 10MB.'))

            # Check file type
            file_extension = resume.name.split('.')[-1].lower()
            if file_extension not in ALLOWED_FILE_TYPES:
                raise ValidationError(_('Invalid file type. Only PDF, DOC, and DOCX files are allowed.'))

        return resume

