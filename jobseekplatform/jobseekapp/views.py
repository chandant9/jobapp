from django.shortcuts import render
# For API 1)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Job, Resume, Application
# For User Registration and User login 2)3)
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
# for login required decorator
from django.contrib.auth.decorators import login_required
# for profile view
from .forms import ProfileForm, LoginForm, JobSearchForm, ResumeUploadForm, JobPostForm, \
    RoleSelectionForm, CandidateRegistrationForm, RecruiterRegistrationForm


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
            cleaned_data = form.cleaned_data
            username = cleaned_data['username']
            email = cleaned_data['email']
            user.save()
    else:
        form = CandidateRegistrationForm()
    return render(request, 'register/candidate_register.html', {'form': form})


def recruiter_register(request):
    if request.method == 'POST':
        form = RecruiterRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            cleaned_data = form.cleaned_data
            username = cleaned_data['username']
            email = cleaned_data['email']
            user.save()
    else:
        form = RecruiterRegistrationForm()
    return render(request, 'register/recruiter_register.html', {'form': form})


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
    return render(request, 'base.html')


@login_required
def profile(request):
    if request.methof == 'POST':
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


@login_required
def home(request):
    return render(request, 'home.html')


def cart_json_view(request):
    cart_data = {
        'item_count': 5,
        'total_price': 100.0,
    }

    return JsonResponse(cart_data)


def job_search(request):
    form = JobSearchForm(request.GET)
    if form.is_valid():
        keyword = form.cleaned_data['keyword']
        location = form.cleaned_data['location']
        jobs = Job.objects.filter(title__icontains=keyword, location__icontains=location)
    else:
        jobs = Job.objects.all()
    return render(request, 'job_search.html', {'jobs': jobs, 'form': form})


def upload_resume(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume = Resume(user=request.user, file=form.cleaned_data['file'])
            resume.save()
            return redirect('resume_upload_success')
    else:
        form = ResumeUploadForm()
    return render(request, 'upload_resume.html', {'form': form})


def job_post(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            return redirect('job_post_success')
    else:
        form = JobPostForm()
    return redirect(request, 'job_post.html', {'form': form})


def apply_job(request, job_id):
    job = Job.objects.get(pk=job_id)

    return redirect('home')
