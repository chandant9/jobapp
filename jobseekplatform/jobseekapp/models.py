from django.db import models
from django.contrib.auth.models import User, Group
import os
from django.utils.text import slugify


# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Profile(models.Model):
    ROLE_CHOICES = (
        ('recruiter', 'Recruiter'),
        ('candidate', 'Candidate')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=25, choices=ROLE_CHOICES, default='')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.user.username


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
    has_questions = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_job_type_display(self):
        return self.job_type.split(',') if self.job_type else []

    def get_schedule_display(self):
        return self.schedule.split(',') if self.schedule else []


class JobQuestion(models.Model):
    QUESTION_TYPES = (
        ('text', 'Text'),
        ('numeric', 'Numeric'),
        ('multiple_choice', 'Multiple Choice'),
        ('radio_button', 'Radio Button'),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='questions')
    question = models.CharField(max_length=300)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    answer = models.TextField(blank=True)

    def __str__(self):
        return self.question


class CandidateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate_profile')
    street_address = models.CharField(max_length=100, blank=True)
    unit_apt_num = models.CharField(max_length=20, blank=True)
    county_district = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=100, blank=True)
    province_state = models.CharField(max_length=100, blank=True)
    zip_postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    education = models.CharField(max_length=255, blank=True)
    work_experience = models.TextField(blank=True)
    phone_num = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username


def resume_file_path(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    unique_filename = f"{slugify(base_filename)}{file_extension}"
    return f"resumes/{unique_filename}"


class Resume(models.Model):
    profile = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='resumes', null=True)
    name = models.CharField(max_length=100, null=True)
    file = models.FileField(upload_to=resume_file_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.id:
            base_filename, file_extension = os.path.splitext(self.file.name)
            unique_filename = f"{slugify(base_filename)}{file_extension}"
            self.file.name = resume_file_path(self, unique_filename)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Resume for {self.file.name}"


class Application(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    cover_letter = models.TextField(null=True, blank=True)
    first_name = models.CharField(max_length=100, default='', blank=True)
    last_name = models.CharField(max_length=100, default='', blank=True)
    email = models.EmailField(default='', blank=True)
    phone_number = models.CharField(max_length=20, default='', blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    resume_file = models.FileField(upload_to='applied_resumes', null=True, blank=True)

    def __str__(self):
        return f"Application for {self.job.title} by {self.applicant.username}"


class CandidateAnswer(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='candidate_answers')
    question = models.ForeignKey(JobQuestion, on_delete=models.CASCADE)
    answer = models.TextField(blank=True)

    def __str__(self):
        return self.answer


# Grant insert privilege to users

class RecruiterGroup(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, primary_key=True, related_name='recruiter_group')
    job_insert_privilege = models.BooleanField(default=False)
    job_question_insert_privilege = models.BooleanField(default=False)

    def __str__(self):
        return self.group.name

    class Meta:
        verbose_name_plural = 'Recruiter Groups'


class CandidateGroup(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, primary_key=True, related_name='candidate_group')
    application_insert_privilege = models.BooleanField(default=False)
    job_answer_insert_privilege = models.BooleanField(default=False)

    def __str__(self):
        return self.group.name

    class Meta:
        verbose_name_plural = 'Candidate Groups'
