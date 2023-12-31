# Generated by Django 4.2.2 on 2023-06-20 20:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jobseekapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='location',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='salary',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='jobseekapp.job'),
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='resumes/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
