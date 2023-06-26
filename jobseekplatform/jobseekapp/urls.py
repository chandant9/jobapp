"""
URL configuration for jobseekplatform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, reverse_lazy
from .views import job_list, login_view, logout_view, base_view, home, profile, \
    change_password, candidate_register, recruiter_register, \
    registration_success, role_selection_view, JobPostingWizardView, JobPostingSuccessView, \
    JobPostingErrorView, job_details, upload_resume, apply_job
from django.contrib.auth import views as auth_views  # built-in password reset functionality
# from . import views  # profile and password change


urlpatterns = [
    path('api/jobs/', job_list, name='job_list'),  # for api endpoints
    path('', base_view, name='base_view'),  # for base
    # path('cart.json', cart_json_view, name='cart_json'),
    path('home/', home, name='home'),  # for home
    path('register/candidate/', candidate_register, name='candidate_register'),
    path('register/recruiter/', recruiter_register, name='recruiter_register'),
    path('register/', role_selection_view, name='register'),
    # path('register/role_selection', role_selection_view, name='role_selection'),  # for user registration
    path('register/registration-success/', registration_success, name='registration_success'),
    path('login/', login_view, name='login'),  # for user login
    path('logout/', logout_view, name='logout'),  # for logout
    # django built-in password reset functionality
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uid64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # for profile and change password views path
    path('profile/', profile, name='profile'),
    path('change-password/', change_password, name='change_password'),
    path('job_posting/<step>/', JobPostingWizardView.as_view(url_name='job_posting_wizard'), name='job_posting_wizard'),
    path('job_posting/success/', JobPostingSuccessView.as_view(), name='job_posting_success'),
    path('company/job_posting/error/', JobPostingErrorView.as_view(), name='job_posting_error'),
    path('job-details/<int:job_id>/', job_details, name='job_details'),
    path('job/application/<int:job_id>/', apply_job, name='apply_job'),
    path('job/resume-upload/', upload_resume, name='upload_resume'),
]
