# from django.contrib import admin
# from django.contrib.auth.admin import GroupAdmin
# from django.contrib.auth.models import Group
# from .models import RecruiterGroup, Job
# from django.contrib.auth.models import Group, Permission
#
# # admin.site.register(Group, GroupAdmin)
#
# admin.site.register(RecruiterGroup)
#
#
# @admin.register(Job)
# class JobAdmin(admin.ModelAdmin):
#     list_display = ['company', 'employee_count', 'recruiter_firstname', 'recruiter_lastname',
#                     'phone', 'country', 'language', 'title', 'job_loctype', 'location',
#                     'job_type', 'schedule', 'start_date_option', 'start_date', 'salary', 'description',
#                     'posted_by', 'created_at', 'updated_at']
#     pass
#
#     def save_model(self, request, obj, form, change):
#         # Call the super method to save the model instance
#         super().save_model(request, obj, form, change)
#
#         # Get the desired group (replace 'Recruiters' with the actual group name)
#         group = Group.objects.get(name='Recruiters')
#
#         # Get the 'add_job' permission
#         permission = Permission.objects.get(codename='add_job')
#
#         # Assign the permission to the group
#         group.permissions.add(permission)
