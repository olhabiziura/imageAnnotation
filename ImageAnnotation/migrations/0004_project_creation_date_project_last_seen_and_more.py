# Generated by Django 5.0.4 on 2025-01-02 19:33

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ImageAnnotation", "0003_project_annotationfields"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="creation_date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="project",
            name="last_seen",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="project",
            name="last_used",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
