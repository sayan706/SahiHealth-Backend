# Generated by Django 4.2.16 on 2024-12-21 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_rename_body_temp_patient_body_temperature_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='speciality',
            field=models.TextField(blank=True, null=True),
        ),
    ]