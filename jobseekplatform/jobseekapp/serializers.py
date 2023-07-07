from rest_framework import serializers
from .models import Job, Application


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title', 'company', 'employee_count', 'country', 'salary', 'job_loctype', 'location', 'job_type', 'schedule', 'start_date', 'description']


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['job', 'applicant', 'first_name', 'last_name', 'email', 'phone_number', 'status', 'resume_file', 'cover_letter', 'applied_at']
