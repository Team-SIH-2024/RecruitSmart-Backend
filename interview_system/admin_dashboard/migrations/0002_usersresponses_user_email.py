# Generated by Django 5.0.6 on 2025-01-04 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersresponses',
            name='user_email',
            field=models.EmailField(default='Not Provided', max_length=254),
        ),
    ]
