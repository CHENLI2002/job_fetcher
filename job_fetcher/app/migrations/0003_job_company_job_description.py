# Generated by Django 5.1.1 on 2024-09-17 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_job_field"),
    ]

    operations = [
        migrations.AddField(
            model_name="job",
            name="company",
            field=models.CharField(default="N/A", max_length=150),
        ),
        migrations.AddField(
            model_name="job",
            name="description",
            field=models.TextField(default="N/A"),
        ),
    ]
