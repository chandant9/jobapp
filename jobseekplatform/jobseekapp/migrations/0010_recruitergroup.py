# Generated by Django 4.2.2 on 2023-06-24 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('jobseekapp', '0009_alter_job_description_alter_job_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecruiterGroup',
            fields=[
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.group')),
                ('job_insert_privilege', models.BooleanField(default=False)),
            ],
        ),
    ]