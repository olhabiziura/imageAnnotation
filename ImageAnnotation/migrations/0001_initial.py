# Generated by Django 5.0.4 on 2024-12-20 18:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                ("projectName", models.CharField(max_length=250)),
                ("projectId", models.AutoField(primary_key=True, serialize=False)),
                ("projectDescription", models.TextField(blank=True, null=True)),
                ("projectFile", models.FileField(blank=True, null=True, upload_to="")),
                (
                    "imageFolder",
                    models.FilePathField(
                        allow_files=False,
                        allow_folders=True,
                        blank=True,
                        max_length=500,
                        null=True,
                        path="/",
                        recursive=True,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="projects",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Image",
            fields=[
                ("imageId", models.AutoField(primary_key=True, serialize=False)),
                ("imageUrl", models.CharField(max_length=500)),
                ("annotation", models.TextField(blank=True, null=True)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="ImageAnnotation.project",
                    ),
                ),
            ],
        ),
    ]
