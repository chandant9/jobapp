from rest_framework import serializers
from .models import Company, Job, Application


class CompanyNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name']


class JobSerializer(serializers.ModelSerializer):
    company = CompanyNameSerializer()
    class Meta:
        model = Job
        fields = ['unique_identifier', 'title', 'company', 'employee_count', 'country', 'salary', 'job_loctype', 'location', 'job_type', 'schedule', 'start_date', 'description']


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['job', 'applicant', 'first_name', 'last_name', 'email', 'phone_number', 'status', 'resume_file', 'cover_letter', 'applied_at']
