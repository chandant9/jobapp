# Generated by Django 4.2.2 on 2023-07-02 16:13

from django.db import migrations


def update_resume_save(apps, schema_editor):
    Resume = apps.get_model('jobseekapp', 'Resume')
    for resume in Resume.objects.all():
        resume.save()


class Migration(migrations.Migration):

    dependencies = [
        ('jobseekapp', '0029_alter_resume_file'),
    ]

    operations = [
        migrations.RunPython(update_resume_save),
    ]
