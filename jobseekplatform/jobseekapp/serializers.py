from rest_framework import serializers
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['job', 'applicant', 'first_name', 'last_name', 'email', 'phone_number', 'status', 'resume_file', 'cover_letter', 'applied_at']
