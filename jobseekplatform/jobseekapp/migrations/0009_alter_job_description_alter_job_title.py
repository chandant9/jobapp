# Generated by Django 4.2.2 on 2023-06-23 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobseekapp', '0008_job_job_type_job_schedule_job_start_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='job',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
