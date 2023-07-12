from rest_framework import serializers
from .models import Company, Job, Application, CandidateProfile


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


class CandidateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateProfile
        fields = ['street_address', 'unit_apt_num', 'county_district', 'city', 'province_state', 'zip_postal_code', 'country', 'education', 'work_experience', 'phone_num']