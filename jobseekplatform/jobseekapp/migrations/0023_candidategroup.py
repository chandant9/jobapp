# Generated by Django 4.2.2 on 2023-06-30 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('jobseekapp', '0022_candidateanswer'),
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
    ]