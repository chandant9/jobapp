# Generated by Django 4.2.2 on 2023-06-27 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobseekapp', '0017_job_has_questions'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=300)),
                ('question_type', models.CharField(choices=[('text', 'Text'), ('numeric', 'Numeric'), ('multiple_choice', 'Multiple Choice'), ('radio_button', 'Radio Button')], max_length=20)),
                ('options', models.TextField(blank=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='jobseekapp.job')),
            ],
        ),
    ]