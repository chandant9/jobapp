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
from .views import logout_view, base_view, home, \
    change_password, candidate_register, recruiter_register, \
    registration_success, role_selection_view, JobPostingWizardView, \
    JobPostingErrorView, job_details, apply_job, CustomLoginView, \
    candidate_profile, view_candidate_profile, view_resumes, delete_resume, \
    applied_jobs, withdraw_application, rename_resume
from django.contrib.auth import views as auth_views  # built-in password reset functionality
# from . import views  # profile and password change
# API VIEW below
from .views import get_job_list, get_job_details, LoginView, LogoutView, get_applied_jobs, \
    get_candidate_profile, update_candidate_profile, create_job
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    # path('api/jobs/', job_list, name='job_list'),  # for api endpoints
    path('', base_view, name='base_view'),  # for base
    # path('cart.json', cart_json_view, name='cart_json'),
    path('home/', home, name='home'),  # for home
    path('register/candidate/', candidate_register, name='candidate_register'),
    path('register/recruiter/', recruiter_register, name='recruiter_register'),
    path('register/', role_selection_view, name='register'),
    # path('register/role_selection', role_selection_view, name='role_selection'),  # for user registration
    path('register/registration-success/', registration_success, name='registration_success'),
    # path('login/', login_view, name='login'),  # for user login
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),  # for logout
    # django built-in password reset functionality
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uid64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # for profile and change password views path
    path('change-password/', change_password, name='change_password'),
    path('job_posting/<step>/', JobPostingWizardView.as_view(url_name='job_posting_wizard'), name='job_posting_wizard'),
    # path('job_posting/success/', JobPostingSuccessView.as_view(), name='job_posting_success'),
    path('company/job_posting/error/', JobPostingErrorView.as_view(), name='job_posting_error'),
    path('job-details/<int:job_id>/', job_details, name='job_details'),
    path('job/application/<int:job_id>/', apply_job, name='apply_job'),
    path('candidate-profile/', candidate_profile, name='candidate_profile'),
    path('view-profile/', view_candidate_profile, name='view_candidate_profile'),
    path('view-resumes/', view_resumes, name='view_resumes'),
    path('delete-resume/<int:resume_id>/', delete_resume, name='delete_resume'),
    path('rename-resume/<int:resume_id>/', rename_resume, name='rename_resume'),
    path('jobs-applied/', applied_jobs, name='applied_jobs'),
    path('application/<int:application_id>/withdraw/', withdraw_application, name='withdraw_application'),
    # API ENDPOINT URLS BELOW ***
    path('api/jobs/', get_job_list, name='get_job_list'),
    path('api/job-details/<unique_identifier>/', get_job_details, name='get_job_details'),
    path('api/role-selection/', csrf_exempt(role_selection_view), name='api_role_selection'),
    path('api/register/candidate/', csrf_exempt(candidate_register), name='api_candidate_register'),
    path('api/register/recruiter/', csrf_exempt(recruiter_register), name='api_recruiter_register'),
    path('api/login/', LoginView.as_view(), name='api_login'),
    path('api/logout/', LogoutView.as_view(), name='api_logout'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/jobs-applied/', get_applied_jobs, name='get_applied_jobs'),
    path('api/candidate-profile/', get_candidate_profile, name='get_candidate_profile'),
    path('api/update-candidate-profile/', update_candidate_profile, name='update_candidate_profile'),
    path('api/jobs/', create_job, name='create_job'),
]
