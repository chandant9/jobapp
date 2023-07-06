from django.shortcuts import render
# For API 1)
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from .models import Job, Resume, Application, Profile, Company, RecruiterGroup, JobQuestion, \
    CandidateAnswer, CandidateGroup, CandidateProfile
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
    CompanyDetailsForm, JobBasicDetailsForm, JobContractDetailsForm, OtherDetailsForm, JobQuestionsFormSet, \
    CandidateProfileForm
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
from django.contrib.auth.views import LoginView
from django.forms import modelformset_factory
from django.core.exceptions import PermissionDenied
from django.core.files import File
import requests
from urllib.parse import urlparse, urlunparse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ApplicationSerializer


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

            group_name = 'Candidates'
            try:
                group = Group.objects.get(name=group_name)
            except Group.DoesNotExist:
                group = Group.objects.create(name=group_name)

            user.groups.add(group)

            # Create or update the CandidateGroup
            candidate_group, created = CandidateGroup.objects.get_or_create(group=group)
            candidate_group.application_insert_privilege = True  # Set the application insert privilege as needed
            candidate_group.job_answer_insert_privilege = True  # Set the answer insert privilege as needed
            candidate_group.save()

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

            # Retrieve or create the Company instance based on the company name
            company_name = form.cleaned_data['company_name']
            company, created = Company.objects.get_or_create(name=company_name)

            profile = Profile(user=user, role='recruiter', company=company)
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
            recruiter_group.job_question_insert_privilege = True  # Set the question insert privilege as needed
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
# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')
#             else:
#                 form.add_error(None, 'Invalid username or password')
#     else:
#         form = LoginForm()
#     return render(request, 'login.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'login.html'  # Replace with your actual login template
    authentication_form = LoginForm

    def get_success_url(self):
        # Customize the success URL after login
        next_url = self.request.GET.get('next')
        if next_url:
            return HttpResponseRedirect(next_url)
        else:
            return reverse_lazy('home')


def logout_view(request):
    logout(request)
    return render(request, 'logout.html')


def base_view(request):
    return render(request, 'home.html')


# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')
#     else:
#         form = ProfileForm(instance=request.user)
#
#     return render(request, 'profile.html', {'form': form})


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


@login_required
def candidate_profile(request):
    user = request.user
    profile = CandidateProfile.objects.get(user=user)

    if request.method == 'POST':
        form = CandidateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_candidate_profile')
    else:
        form = CandidateProfileForm(instance=profile)

    context = {
        'form': form,
        'profile': profile
    }
    return render(request, 'profiles/candidate_profile.html', context)


@login_required
def view_candidate_profile(request):
    user = request.user
    profile, created = CandidateProfile.objects.get_or_create(user=user)
    latest_resume = profile.resumes.latest('uploaded_at') if profile.resumes.exists() else None

    form = CandidateProfileForm(instance=profile)

    context = {
        'profile': profile,
        'latest_resume': latest_resume,
        'form': form
    }
    return render(request, 'profiles/view_candidate_profile.html', context)


@login_required
def view_resumes(request):
    profile = request.user.candidate_profile  # Get the candidate profile for the current user
    resumes = profile.resumes.order_by('-uploaded_at')  # Sort resumes by uploaded_at in descending order

    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.profile = profile
            resume.save()
            return redirect('view_resumes')
    else:
        form = ResumeUploadForm()

    # Check if the query parameter 'from_job_application' is present
    from_job_application = bool(request.GET.get('from_job_application'))

    context = {
        'resumes': resumes,
        'form': form,
        'from_job_application': from_job_application
    }
    return render(request, 'profiles/view_resumes.html', context)


@login_required
def delete_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)

    # Check if the resume belongs to the current user
    if resume.profile.user != request.user:
        raise PermissionDenied

    # Delete the resume
    resume.delete()

    return redirect('view_resumes')


@login_required
def rename_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)

    # Check if the resume belongs to the current user
    if resume.profile.user != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        new_name = request.POST.get('new_name')
        resume.name = new_name
        resume.save()
        return redirect('view_resumes')

    return redirect('view_resumes')


def apply_job(request, job_id):
    job = Job.objects.get(id=job_id)
    user = request.user

    if Application.objects.filter(job=job, applicant=user).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('applied_jobs')

    # Retrieve the user's candidate profile
    candidate_profile, created = CandidateProfile.objects.get_or_create(user=user)

    # Retrieve the user's uploaded resumes
    user_resumes = candidate_profile.resumes.all()
    # Retrieve the latest uploaded resume
    latest_resume = Resume.objects.order_by('-uploaded_at').first()

    if request.method == 'POST':
        if 'attach-resume' in request.POST:
            return redirect(reverse('view_resumes') + '?from_job_application=1')

        form = JobApplicationForm(request.POST, request.FILES, job=job, user=user)

        if form.is_valid():
            job_application = form.save(commit=False)
            job_application.job = job
            job_application.applicant = user
            resume_file = form.cleaned_data.get('resume_file')

            job_application.resume_file = resume_file

            job_application.save()

            for question in job.questions.all():
                answer = form.cleaned_data.get(f'question_{question.id}')
                CandidateAnswer.objects.create(application=job_application, question=question, answer=answer)

            messages.success(request, 'Job application submitted successfully.')
            return redirect('applied_jobs')
    else:
        form = JobApplicationForm(job=job, user=user)

    form.initial['job'] = job  # Set the initial value for the job field
    form.fields['resume_file'].queryset = user_resumes  # Set the queryset for the resume_file field

    context = {
        'form': form,
        'job': job,
        'user_resumes': user_resumes,
        'from_job_application': True,
        'latest_resume': latest_resume
    }
    return render(request, 'job/apply_job.html', context)


def applied_jobs(request):
    user = request.user
    applications = Application.objects.filter(applicant=user).order_by('-applied_at')
    return render(request, 'job/applied_jobs.html', {'applications': applications})


def withdraw_application(request, application_id):
    application = Application.objects.get(id=application_id)

    if application.applicant != request.user:
        return HttpResponseForbidden()

    if application.status == 'withdrawn':
        messages.warning(request, 'This application has already been withdrawn.')
    else:
        application.status = 'withdrawn'
        application.save()
        messages.success(request, 'Application withdrawn successfully.')

    return redirect('applied_jobs')


# Job Posting view
class JobPostingWizardView(SuccessMessageMixin, NamedUrlSessionWizardView):
    template_name = 'company/job_posting.html'
    url_name = 'job_posting_wizard'

    form_list = [
        ('company_details', CompanyDetailsForm),
        ('job_basic', JobBasicDetailsForm),
        ('job_contract', JobContractDetailsForm),
        ('other_details', OtherDetailsForm),
        ('job_questions', JobQuestionsFormSet),
    ]

    def get_form_initial(self, step):
        initial = self.initial_dict.get(step, {})
        if step == 'company_details':
            registered_company_name = self.request.user.profile.company
            initial['company'] = registered_company_name
        return initial

    def done(self, form_list, **kwargs):
        form_data = {}
        for form in form_list:
            if isinstance(form, JobQuestionsFormSet):
                form_data['job_questions'] = []
                for formset_form in form:
                    if formset_form.cleaned_data:
                        form_data['job_questions'].append(formset_form.cleaned_data)
            elif hasattr(form, 'cleaned_data'):
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
                has_questions=form_data['has_questions'],
                posted_by=self.request.user,
                created_at=timezone.now(),
                updated_at=timezone.now(),
                # Add more attributes as needed
            )

            # Save the job questions
            job_question_data = form_data.get('job_questions')
            if job_question_data:
                for question_data in job_question_data:
                    question = question_data.get('question')
                    question_type = question_data.get('question_type')
                    answer = question_data.get('answer')

                    JobQuestion.objects.create(
                        job=job,
                        question=question,
                        question_type=question_type,
                        answer=answer
                    )
            else:
                messages.error(self.request, "Invalid job questions formset data.")
                return redirect('job_posting_error')

            job_id = job.id

            # Store the job ID in the session for future reference if needed
            self.request.session['job_id'] = job_id

            return render(self.request, 'company/job_posting_success.html',
                          {'form_data': form_data})
        else:
            messages.error(self.request, "You do not have permission to post a job.")
            return redirect('job_posting_error')

    def has_insert_access(self):
        recruiters_group = Group.objects.get(name='Recruiters')
        if recruiters_group in self.request.user.groups.all():
            recruiter_group = RecruiterGroup.objects.get(group=recruiters_group)
            return recruiter_group.job_insert_privilege and recruiter_group.job_question_insert_privilege
        return False

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class JobPostingErrorView(TemplateView):
    template_name = 'company/job_posting_error.html'


# ******* API END POINT VIEWS FROM BELOW *******

def get_job_list(request):
    # Fetch the job list from the database or data source
    jobs = Job.objects.all()

    # Convert the job list to a serialized JSON response
    job_list = []
    for job in jobs:
        job_list.append({
            'id': job.id,
            'title': job.title,
            'job_loctype': job.job_loctype,
            'company': job.company,
            'country': job.country,
            'salary': job.salary,
            'job_type': job.job_type,
            'description': job.description,
            # Add other job properties as needed
        })

    # Return the jobs data as a JSON response
    return JsonResponse({'jobs': job_list})


@api_view(['GET'])
def get_applied_jobs(request):
    # Retrieve the currently signed-in user
    user = request.user

    # Retrieve the applied jobs for the user
    applications = user.applications.all()

    # Serialize the application data
    serializer = ApplicationSerializer(applications, many=True)

    return Response(serializer.data)
