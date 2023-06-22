from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Job, Resume, Application
# for resume validation check
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# for django built-in country and country specific language choices
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
import pycountry


# defined for Resume validation check in JobApplicationForm class
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_FILE_TYPES = ['pdf', 'doc', 'docx']
# defined for CompanyDetailsForm class
EMPLOYEE_COUNT_CHOICES = [
    ('1-10', '1 to 10'),
    ('11-50', '11 to 50'),
    ('51-100', '51 to 100'),
    ('101-150', '101 to 150'),
    ('151-250', '151 to 250'),
    ('251-350', '251 to 350'),
    ('351-550', '351 to 550'),
    ('551-1000', '551 to 1000'),
    ('1001-1500', '1001 to 1500'),
    ('1501-2000', '1501 to 2000'),
    ('2000+', '2000+'),
]
# defined for JobBasicDetailsForm class
LOCATION_TYPE_CHOICES = [
    ('Remote', ' Work from Home'),
    ('Hybrid', 'Combination of work from physical assigned location and from Home'),
    ('Physical location', 'Need to be available physically at work location'),
    ('Outdoors', 'Need to always be on the road, travel'),
]

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


# Job posting forms

class CompanyDetailsForm(forms.Form):
    company_name = forms.CharField(max_length=100, disabled=True)
    employee_count = forms.ChoiceField(choices=EMPLOYEE_COUNT_CHOICES)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    phone_number = forms.CharField(max_length=20)

    def __init__(self, *args, **kwargs):
        initial_company_name = kwargs.pop('company_name', '')
        super(CompanyDetailsForm, self).__init__(*args, **kwargs)
        self.initial['job_company_name'] = initial_company_name

    # function to edit company name and keep the registered company name if not edited
    def clean_job_company_name(self):
        job_company_name = self.cleaned_data.get('job_company_name')
        if job_company_name:
            return job_company_name.strip()
        return ''


class JobBasicDetailsForm(forms.Form):
    country = CountryField().formfield(widget=CountrySelectWidget)
    language = forms.ChoiceField(choices=[
                (lang.alpha_2, lang.name)
                for lang in pycountry.languages
                ], widget=forms.Select)
    job_title = forms.CharField(max_length=100)
    location_type = forms.ChoiceField(choices=LOCATION_TYPE_CHOICES)
    job_address = forms.CharField(max_length=100)
    language_requirement = forms.CharField(max_length=100)
    language_training_provided = forms.BooleanField(required=False)


