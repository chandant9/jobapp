from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Job, Resume, Application, Profile
# for resume validation check
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# for django built-in country and country specific language choices
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
import pycountry
from multiselectfield import MultiSelectFormField



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


# Job posting forms
        return resume


class CompanyDetailsForm(forms.ModelForm):
    company = forms.CharField(max_length=100, required=False)
    employee_count = forms.ChoiceField(choices=EMPLOYEE_COUNT_CHOICES, required=False)
    recruiter_firstname = forms.CharField(max_length=50)
    recruiter_lastname = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=20)

    class Meta:
        model = Job
        fields = ['company', 'employee_count', 'recruiter_firstname', 'recruiter_lastname', 'phone']


class JobBasicDetailsForm(forms.ModelForm):
    country = CountryField().formfield(widget=CountrySelectWidget)
    language = forms.ChoiceField(choices=[], widget=forms.Select)
    title = forms.CharField(max_length=100)
    job_loctype = forms.ChoiceField(choices=LOCATION_TYPE_CHOICES, required=False)
    location = forms.CharField(max_length=100, required=False)
    # language_requirement = forms.CharField(max_length=100)
    # language_training_provided = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Generate language choices based on major spoken languages for each country
        language_choices = []
        for country in pycountry.countries:
            languages = pycountry.languages.get(alpha_2=country.alpha_2)
            if languages:
                language_choices.append((languages.alpha_3, languages.name))

        self.fields['language'].choices = language_choices

    class Meta:
        model = Job
        fields = ['country', 'language', 'title', 'job_loctype', 'location']


class JobContractDetailsForm(forms.ModelForm):
    job_type = forms.MultipleChoiceField(choices=Job.JOB_TYPE_CHOICES, widget=forms.CheckboxSelectMultiple)
    schedule = forms.MultipleChoiceField(choices=Job.SCHEDULE_CHOICES, widget=forms.CheckboxSelectMultiple)
    start_date_option = forms.ChoiceField(
        label='Start Date Option',
        choices=[('no', 'No'), ('yes', 'Yes')],
        widget=forms.RadioSelect,
        initial='no'
    )
    start_date = forms.DateField(
        label='Start Date',
        widget=forms.DateInput(attrs={'class': 'datepicker'}),
        required=False
    )

    class Meta:
        model = Job
        fields = ['job_type', 'schedule', 'start_date_option', 'start_date']


class OtherDetailsForm(forms.ModelForm):
    description = forms.CharField(max_length=250, required=False)
    salary = forms.DecimalField(max_digits=8, decimal_places=2, required=False)

    class Meta:
        model = Job
        fields = ['salary', 'description']



