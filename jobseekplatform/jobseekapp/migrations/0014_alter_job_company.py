# Generated by Django 4.2.2 on 2023-06-25 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobseekapp', '0013_auto_20230624_2230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='company',
            field=models.CharField(default='', max_length=100),
        ),
    ]