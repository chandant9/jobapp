from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Job, Resume, Application, Profile, Company, JobQuestion, CandidateProfile
# for resume validation check
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# for django built-in country and country specific language choices
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
import pycountry
from multiselectfield import MultiSelectFormField
from django.conf import settings
from django.forms import formset_factory
import os


# defined for Resume validation check in JobApplicationForm class
MAX_FILE_SIZE = settings.MAX_RESUME_FILE_SIZE
ALLOWED_FILE_TYPES = settings.ALLOWED_RESUME_FILE_TYPES
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


class LoginForm(AuthenticationForm):
    pass


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

    def clean(self):
        cleaned_data = super().clean()

        company_name = cleaned_data.get('company_name')

        # Check for anomalies or additional validation
        if company_name and company_name.isnumeric():
            raise forms.ValidationError("Company name should not be a numeric value.")

        return cleaned_data


class JobSearchForm(forms.Form):
    keyword = forms.CharField(max_length=100, required=False)
    location = forms.CharField(max_length=100, required=False)


class ResumeUploadForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = Resume
        fields = ['name', 'file']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Check file size
            if file.size > MAX_FILE_SIZE:
                raise forms.ValidationError(f'File size exceeds the maximum limit of {MAX_FILE_SIZE / (1024 * 1024)}MB.')

            # Check file type
            file_extension = file.name.split('.')[-1].lower()
            print(file_extension)
            if file_extension not in ALLOWED_FILE_TYPES:
                raise forms.ValidationError('Invalid file type. Only PDF, DOC, and DOCX files are allowed.')

        return file


class CandidateProfileForm(forms.ModelForm):
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    resume = forms.FileField(required=False)

    class Meta:
        model = CandidateProfile
        fields = ['username', 'first_name', 'last_name', 'street_address', 'unit_apt_num', 'county_district', 'city',
                  'province_state', 'zip_postal_code', 'country', 'education',
                  'work_experience', 'phone_num', 'resume']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].initial = self.instance.user.username
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            profile.save()
            user.save()

            # Handle uploaded resume
            resume = self.cleaned_data.get('resume')
            if resume:
                Resume.objects.create(profile=profile, file=resume)

        return profile


class JobApplicationForm(forms.ModelForm):
    existing_resume = forms.ModelChoiceField(queryset=Resume.objects.none(), required=False,
                                             empty_label='Select an existing resume')
    new_resume = forms.FileField(required=False)

    def __init__(self, *args, **kwargs):
        job = kwargs.pop('job')
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        candidate_profile = CandidateProfile.objects.get(user=user)
        self.fields['existing_resume'].queryset = candidate_profile.resumes.all()

        job_questions = job.questions.all()

        for question in job_questions:
            field_name = f'question_{question.id}'

            if question.question_type == 'text':
                self.fields[field_name] = forms.CharField(
                    label=question.question,
                    max_length=255
                )
            elif question.question_type == 'numeric':
                self.fields[field_name] = forms.IntegerField(
                    label=question.question
                )
            elif question.question_type in ['multiple_choice', 'radio_button']:
                choices = [(option.strip(), option.strip()) for option in question.answer_options.split(',')]
                self.fields[field_name] = forms.ChoiceField(
                    label=question.question,
                    choices=choices,
                    widget=forms.RadioSelect
                )
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name
        self.fields['email'].initial = user.email
        self.fields['phone_number'].initial = candidate_profile.phone_num

    class Meta:
        model = Application
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'existing_resume', 'new_resume', 'cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 5}),
        }

    def clean(self):
        cleaned_data = super().clean()
        existing_resume = cleaned_data.get('existing_resume')
        new_resume = cleaned_data.get('new_resume')

        if not existing_resume and not new_resume:
            raise forms.ValidationError('Please select an existing resume or upload a new resume.')
        elif existing_resume and new_resume:
            raise forms.ValidationError("Please select only one option: existing resume or new resume.")

        # Check file size
        if new_resume:
            if new_resume.size > MAX_FILE_SIZE:
                raise forms.ValidationError(f'File size exceeds the maximum limit of {MAX_FILE_SIZE / (1024 * 1024)}MB.')

            # Check file type
            file_extension = new_resume.name.split('.')[-1].lower()
            if file_extension not in ALLOWED_FILE_TYPES:
                raise forms.ValidationError('Invalid file type. Only PDF, DOC, and DOCX files are allowed.')

        return cleaned_data


# Job Posting Forms
class CompanyDetailsForm(forms.ModelForm):
    company = forms.CharField(max_length=100, required=False, disabled=True)
    employee_count = forms.ChoiceField(choices=EMPLOYEE_COUNT_CHOICES, required=False)
    recruiter_firstname = forms.CharField(max_length=50)
    recruiter_lastname = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=20)

    class Meta:
        model = Job
        fields = ['company', 'employee_count', 'recruiter_firstname', 'recruiter_lastname', 'phone']

    def clean(self):
        cleaned_data = super().clean()

        # Perform additional validation checks here
        # For example, if phone number must be numeric:
        phone = cleaned_data.get('phone')
        if phone and not phone.isnumeric():
            raise ValidationError("Phone number should only contain numeric characters.")

        company_name = cleaned_data.get('company')
        company, _ = Company.objects.get_or_create(name=company_name)

        cleaned_data['company'] = company

        return cleaned_data


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

    def clean(self):
        cleaned_data = super().clean()

        # Perform additional validation checks here
        # For example, if title must not contain certain characters:
        title = cleaned_data.get('title')
        if title and any(char in title for char in ['!', '@', '#']):
            raise ValidationError("Title should not contain special characters.")

        return cleaned_data


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

    def clean(self):
        cleaned_data = super().clean()

        # Perform additional validation checks here

        return cleaned_data


class OtherDetailsForm(forms.ModelForm):
    description = forms.CharField(max_length=250, required=False)
    salary = forms.DecimalField(max_digits=8, decimal_places=2, required=False)
    has_questions = forms.BooleanField(label='Add job-specific questions', required=False)

    class Meta:
        model = Job
        fields = ['salary', 'description', 'has_questions']

    def clean(self):
        cleaned_data = super().clean()
        has_questions = cleaned_data.get('has_questions')
        description = cleaned_data.get('description')
        salary = cleaned_data.get('salary')

        if has_questions and (not description or not salary):
            raise forms.ValidationError("Please provide a description and salary before adding job-specific questions.")

        return cleaned_data


class JobQuestionsForm(forms.ModelForm):
    class Meta:
        model = JobQuestion
        fields = ['question', 'question_type', 'answer']


JobQuestionsFormSet = formset_factory(JobQuestionsForm, extra=2)

    # def clean_answer(self):
    #     question_type = self.cleaned_data.get('question_type')
    #     answer = self.cleaned_data.get('answer')
    #
    #     if question_type == 'multiple_choice' or question_type == 'radio_button':
    #         if answer and ',' not in answer:
    #             raise forms.ValidationError("For multiple choice or radio button question types, the answer should have at least two options separated by commas.")
    #     elif question_type == 'text' or question_type == 'numeric':
    #         if answer:
    #             raise forms.ValidationError("The answer field should be left blank for text or numeric question types.")
    #
    #     return answer
