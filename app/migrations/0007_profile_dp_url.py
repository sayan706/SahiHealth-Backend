# Generated by Django 4.2.16 on 2024-12-15 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_profile_email_alter_profile_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='dp_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
