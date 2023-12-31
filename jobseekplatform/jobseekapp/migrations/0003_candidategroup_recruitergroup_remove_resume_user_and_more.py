# Generated by Django 4.2.2 on 2023-07-03 15:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jobseekapp.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('jobseekapp', '0002_job_location_job_salary_alter_application_job_resume'),
    ]

    operations = [
        migrations.CreateModel(
            name='CandidateGroup',
            fields=[
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='candidate_group', serialize=False, to='auth.group')),
                ('application_insert_privilege', models.BooleanField(default=False)),
                ('job_answer_insert_privilege', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Candidate Groups',
            },
        ),
        migrations.CreateModel(
            name='RecruiterGroup',
            fields=[
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='recruiter_group', serialize=False, to='auth.group')),
                ('job_insert_privilege', models.BooleanField(default=False)),
                ('job_question_insert_privilege', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Recruiter Groups',
            },
        ),
        migrations.RemoveField(
            model_name='resume',
            name='user',
        ),
        migrations.AddField(
            model_name='application',
            name='cover_letter',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254),
        ),
        migrations.AddField(
            model_name='application',
            name='first_name',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='application',
            name='last_name',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='application',
            name='phone_number',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AddField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('withdrawn', 'Withdrawn')], default='pending', max_length=10),
        ),
        migrations.AddField(
            model_name='job',
            name='country',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='job',
            name='employee_count',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='job',
            name='has_questions',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='job',
            name='job_loctype',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='job',
            name='job_type',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='job',
            name='language',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='job',
            name='phone',
            field=models.CharField(default='', max_length=25),
        ),
        migrations.AddField(
            model_name='job',
            name='recruiter_firstname',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='job',
            name='recruiter_lastname',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='job',
            name='schedule',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='job',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='start_date_option',
            field=models.CharField(choices=[('no', 'No'), ('yes', 'Yes')], default='no', max_length=3),
        ),
        migrations.AddField(
            model_name='resume',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='job',
            name='salary',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='title',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='resume',
            name='file',
            field=models.FileField(upload_to=jobseekapp.models.resume_file_path),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('recruiter', 'Recruiter'), ('candidate', 'Candidate')], default='', max_length=25)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jobseekapp.company')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='JobQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=300)),
                ('question_type', models.CharField(choices=[('text', 'Text'), ('numeric', 'Numeric'), ('multiple_choice', 'Multiple Choice'), ('radio_button', 'Radio Button')], max_length=20)),
                ('answer', models.TextField(blank=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='jobseekapp.job')),
            ],
        ),
        migrations.CreateModel(
            name='CandidateProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address', models.CharField(blank=True, max_length=100)),
                ('unit_apt_num', models.CharField(blank=True, max_length=20)),
                ('county_district', models.CharField(blank=True, max_length=50)),
                ('city', models.CharField(blank=True, max_length=100)),
                ('province_state', models.CharField(blank=True, max_length=100)),
                ('zip_postal_code', models.CharField(blank=True, max_length=20)),
                ('country', models.CharField(blank=True, max_length=100)),
                ('education', models.CharField(blank=True, max_length=255)),
                ('work_experience', models.TextField(blank=True)),
                ('phone_num', models.CharField(blank=True, max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='candidate_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CandidateAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(blank=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidate_answers', to='jobseekapp.application')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobseekapp.jobquestion')),
            ],
        ),
        migrations.AddField(
            model_name='resume',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='resumes', to='jobseekapp.candidateprofile'),
        ),
    ]
