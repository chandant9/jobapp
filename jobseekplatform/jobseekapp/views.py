from django.shortcuts import render
# For API 1)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Job, Resume, Application, Profile, Company, RecruiterGroup
# For User Registration and User login 2)3)
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
# for login required decorator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# for profile view
from .forms import ProfileForm, LoginForm, JobSearchForm, ResumeUploadForm, \
    RoleSelectionForm, CandidateRegistrationForm, RecruiterRegistrationForm, JobApplicationForm, \
    CompanyDetailsForm, JobBasicDetailsForm, JobContractDetailsForm, OtherDetailsForm
from django.contrib import messages
from formtools.wizard.views import NamedUrlSessionWizardView
from django.contrib.auth.models import User
from django.views import View
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView
import logging
from django.utils import timezone
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse

# defined for JobPostingWizardView
JOB_POSTING_FORMS = [
    ("company_details", CompanyDetailsForm),
    ("job_basic", JobBasicDetailsForm),
    ("job_contract", JobContractDetailsForm),
    # Add more form steps here
]


# Create your views here.

# 1) Setting up api endpoints for the platform
@csrf_exempt
def job_list(request):
    if request.method == 'GET':
        jobs = Job.objects.all()
        job_data = [{'title': job.title, 'description': job.description} for job in jobs]
        return JsonResponse({'jobs': job_data})

    elif request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        job = Job.objects.create(title=title, description=description)
        return JsonResponse({'message': 'Job created successfully'})


# 2) User registration

def role_selection_view(request):
    if request.method == 'POST':
        form = RoleSelectionForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            if role == 'candidate':
                return redirect('candidate_register')
            elif role == 'recruiter':
                return redirect('recruiter_register')
    else:
        form = RoleSelectionForm()

    return render(request, 'register/role_selection.html', {'form': form})


def candidate_register(request):
    if request.method == 'POST':
        form = CandidateRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            profile = Profile(user=user, role='candidate')
            profile.save()

            messages.success(request, 'Registration successful. Please log in.')
            return redirect('registration_success')
    else:
        form = CandidateRegistrationForm()
    return render(request, 'register/candidate_register.html', {'form': form})


def recruiter_register(request):
    if request.method == 'POST':
        form = RecruiterRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            company_name = form.cleaned_data['company_name']
            profile = Profile(user=user, role='recruiter', company_name=company_name)
            profile.save()

            group_name = 'Recruiters'
            try:
                group = Group.objects.get(name=group_name)
            except Group.DoesNotExist:
                group = Group.objects.create(name=group_name)

            user.groups.add(group)

            # Create or update the RecruiterGroup
            recruiter_group, created = RecruiterGroup.objects.get_or_create(group=group)
            recruiter_group.job_insert_privilege = True  # Set the job insert privilege as needed
            recruiter_group.save()

            # Grant the add_job permission to the user
            # content_type = ContentType.objects.get_for_model(Job)
            # permission = Permission.objects.get(content_type=content_type, codename='add_job')
            # user.user_permissions.add(permission)

            messages.success(request, 'Registration successful. Please log in.')
            return redirect('registration_success')
    else:
        form = RecruiterRegistrationForm()
    return render(request, 'register/recruiter_register.html', {'form': form})


def registration_success(request):
    return render(request, 'register/registration_success.html')


# 3) User login
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'logout.html')


def base_view(request):
    return render(request, 'home.html')


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'profile.html', {'form': form})


@login_required
def update_profile(request):
    return render(request, 'update_profile.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('change_password')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'change_password.html', {'form': form})


def home(request):
    form = JobSearchForm(request.GET)
    if form.is_valid():
        keyword = form.cleaned_data['keyword']
        location = form.cleaned_data['location']
        if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.role == 'recruiter':
            jobs = Job.objects.filter(posted_by=request.user, title__icontains=keyword, location__icontains=location)
        else:
            jobs = Job.objects.filter(title__icontains=keyword, location__icontains=location)
    else:
        if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.role == 'recruiter':
            jobs = Job.objects.filter(posted_by=request.user)
        else:
            jobs = Job.objects.all()

    context = {
        'jobs': jobs,
        'form': form,
    }

    if request.user.is_authenticated:
        context['username'] = request.user.username

    return render(request, 'home.html', context)


# def cart_json_view(request):
#     cart_data = {
#         'item_count': 5,
#         'total_price': 100.0,
#     }
#
#     return JsonResponse(cart_data)


def job_details(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'job_details.html', {'job': job})


def upload_resume(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume = Resume(user=request.user, file=form.cleaned_data['file'])
            resume.save()
            return redirect('resume_upload_success')
    else:
        form = ResumeUploadForm()
    return render(request, 'job/upload_resume.html', {'form': form})


def apply_job(request, job_id):
    job = Job.objects.get(id=job_id)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            job_application = form.save(commit=False)
            job_application.job = job
            job_application.save()

            messages.success(request, 'Job application submitted successfully.')
            return redirect('home')
    else:
        form = JobApplicationForm()

    context = {
        'form': form,
        'job': job
    }
    return render(request, 'job/apply_job.html', context)


# Job Posting view
class JobPostingWizardView(SuccessMessageMixin, NamedUrlSessionWizardView):
    template_name = 'company/job_posting.html'
    url_name = 'job_posting_wizard'
    form_list = [
        ('company_details', CompanyDetailsForm),
        ('job_basic', JobBasicDetailsForm),
        ('job_contract', JobContractDetailsForm),
        ('other_details', OtherDetailsForm)
    ]

    # success_url = reverse_lazy('job_posting_success')
    # success_message = "Job posting submitted successfully."

    def get_form_initial(self, step):
        initial = self.initial_dict.get(step, {})
        if step == 'company_details':
            registered_company_name = self.request.user.profile.company_name
            initial['company'] = registered_company_name
        return initial

    def done(self, form_list, **kwargs):
        form_data = {}
        for form in form_list:
            if hasattr(form, 'cleaned_data'):
                form_data.update(form.cleaned_data)
            else:
                form_data.update(form.data)

        # Check if the user has insert access
        if self.has_insert_access():
            job = Job.objects.create(
                # CompanyDetailsForm (1)
                company=form_data['company'],
                employee_count=form_data['employee_count'],
                recruiter_firstname=form_data['recruiter_firstname'],
                recruiter_lastname=form_data['recruiter_lastname'],
                phone=form_data['phone'],
                # JobBasicDetailsForm (2)
                country=form_data['country'],
                language=form_data['language'],
                title=form_data['title'],
                job_loctype=form_data['job_loctype'],
                location=form_data['location'],
                # JobContractDetailsForm (3)
                job_type=form_data['job_type'],
                schedule=form_data['schedule'],
                start_date_option=form_data['start_date_option'],
                start_date=form_data['start_date'],
                # to be added
                description=form_data['description'],
                salary=form_data['salary'],
                posted_by=self.request.user,
                created_at=timezone.now(),
                updated_at=timezone.now(),
                # Add more attributes as needed
            )
            job_id = job.id

            # Store the job ID in the session for future reference if needed
            self.request.session['job_id'] = job_id

            return render(self.request, 'job_posting_success', {'form_data': [form.cleaned_data for form in form_list]})
        else:
            messages.error(self.request, "You do not have permission to post a job.")
            return redirect('job_posting_error')

    def has_insert_access(self):
        recruiters_group = Group.objects.get(name='Recruiters')
        if recruiters_group in self.request.user.groups.all():
            recruiter_group = RecruiterGroup.objects.get(group=recruiters_group)
            return recruiter_group.job_insert_privilege
        return False

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class JobPostingErrorView(TemplateView):
    template_name = 'company/job_posting_error.html'


class JobPostingSuccessView(TemplateView):
    template_name = 'company/job_posting_success.html'
