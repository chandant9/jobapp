from django.shortcuts import render
# For API 1)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from jobseekplatform.jobseekapp.models import Job
# For User Registration 2)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

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
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
