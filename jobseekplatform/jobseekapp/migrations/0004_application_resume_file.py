# Generated by Django 4.2.2 on 2023-07-03 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobseekapp', '0003_candidategroup_recruitergroup_remove_resume_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='resume_file',
            field=models.FileField(blank=True, null=True, upload_to='applied_resumes'),
        ),
    ]