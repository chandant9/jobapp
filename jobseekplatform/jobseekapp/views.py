from django.shortcuts import render
# For API 1)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Job
# For User Registration and User login 2)3)
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
# for login required decorator
from django.contrib.auth.decorators import login_required
# for profile view
from .forms import ProfileForm, LoginForm, RegistrationForm


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
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            username = cleaned_data['username']
            email = cleaned_data['email']
            password = cleaned_data['password1']
            form.save()
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


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
