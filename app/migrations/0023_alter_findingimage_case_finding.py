# Generated by Django 4.2.16 on 2025-01-16 04:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_casefinding_severity_findingimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='findingimage',
            name='case_finding',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='finding_images', to='app.casefinding'),
        ),
    ]