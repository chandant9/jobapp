from django.db import models
from django.contrib.auth.models import User


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
    title = models.CharField(max_length=200)
    description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=100, null=True)
    job_loctype = models.CharField(max_length=100, default='')
    salary = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    employee_count = models.CharField(max_length=50, default='')
    recruiter_firstname = models.CharField(max_length=50, default='')
    recruiter_lastname = models.CharField(max_length=50, default='')
    phone = models.CharField(max_length=25, default='')
    country = models.CharField(max_length=50, default='')
    language = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.title


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    resume = models.FileField(upload_to='resumes/', default='')
    cover_letter = models.TextField(null = True, blank=True)

    def __str__(self):
        return f"Application for {self.job.title} by {self.applicant.username}"


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resume for {self.user.username}"

