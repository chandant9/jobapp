from django.db import models
from django.contrib.auth.models import User, Group
# from multiselectfield import MultiSelectField


# Used in profile model below

class Profile(models.Model):
    ROLE_CHOICES = (
        ('recruiter', 'Recruiter'),
        ('candidate', 'Candidate')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=25, choices=ROLE_CHOICES, default='')
    company_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username


# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Job(models.Model):
    # Default //
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # CompanyDetailsForm (1)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    employee_count = models.CharField(max_length=50, default='')
    recruiter_firstname = models.CharField(max_length=50, default='')
    recruiter_lastname = models.CharField(max_length=50, default='')
    phone = models.CharField(max_length=25, default='')

    # JobBasicDetailsForm (2)
    country = models.CharField(max_length=50, default='')
    language = models.CharField(max_length=50, default='')
    title = models.CharField(max_length=100)
    job_loctype = models.CharField(max_length=100, default='')
    location = models.CharField(max_length=100, null=True)

    # JobContractDetailsForm (3)
    JOB_TYPE_CHOICES = (
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('casual', 'Casual'),
        ('permanent', 'Permanent'),
        ('temporary', 'Temporary'),
        ('fixed_term', 'Fixed Term'),
        ('freelance', 'Freelance'),
        ('apprenticeship', 'Apprenticeship'),
        ('seasonal', 'Seasonal'),
        ('internship', 'Internship'),
    )
    job_type = models.CharField(max_length=150, blank=True)
    SCHEDULE_CHOICES = (
        ('mon-fri', 'Monday to Friday'),
        ('day_shift', 'Day shift'),
        ('night_shift', 'Night shift'),
        ('mor_shift', 'Morning shift'),
        ('eve_shift', 'Evening shift'),
        ('weekend_avail', 'Weekend availability'),
        ('overtime', 'Overtime'),
        ('8_hr_shift', '8 hour shift'),
        ('12_hr_shift', '12 hour shift'),
        ('4_hr_shift', '4 hour shift'),
        ('on_call', 'On Call'),
    )
    schedule = models.CharField(max_length=150, blank=True)
    start_date_option = models.CharField(max_length=3, choices=[('no', 'No'), ('yes', 'Yes')], default='no')
    start_date = models.DateField(null=True, blank=True)

    # TO BE ASSIGNED
    description = models.TextField(default='')  # to be assigned
    salary = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)  # to be assigned

    def __str__(self):
        return self.title

    def get_job_type_display(self):
        return self.job_type.split(',') if self.job_type else []

    def get_schedule_display(self):
        return self.schedule.split(',') if self.schedule else []


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    resume = models.FileField(upload_to='resumes/', default='')
    cover_letter = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Application for {self.job.title} by {self.applicant.username}"


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resume for {self.user.username}"


# Grant insert privilege to users

class RecruiterGroup(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, primary_key=True)
    job_insert_privilege = models.BooleanField(default=False)

    def __str__(self):
        return self.group.name