from django.db import models
from django.contrib.auth.models import User
from django.db.models import Manager
from django.utils.timezone import now

class ProjectManager(Manager):
    def get(self, *args, **kwargs):
        project = super().get(*args, **kwargs)
        project.update_annotation_fields()  # Update annotation fields on access
        return project
    
class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    projectName = models.CharField(max_length=250)
    projectId = models.AutoField(primary_key=True)
    projectDescription = models.TextField(blank=True, null=True)
    projectFile = models.FileField(blank=True, null=True)
    annotationFields = models.JSONField(default=list, blank=True, null=True)

    last_used = models.DateTimeField(blank=True, null=True)
    creation_date = models.DateTimeField(default=now)  # Set default to current timestamp
    last_seen = models.DateTimeField(blank=True, null=True)

    objects = ProjectManager()

    def __str__(self):
        return f"{self.projectName} by {self.user.username}"

    def update_annotation_fields(self):
        # Get the unique set of all annotations from the images associated with this project
        annotations = set(image.annotation for image in self.images.all() if image.annotation)

        # Add new annotations that are not already in the annotationFields
        current_annotations = set(self.annotationFields or [])

        new_annotations = annotations - current_annotations
 
        # Add any new annotations to the list
        if new_annotations:
            self.annotationFields = list(current_annotations.union(new_annotations))
            self.save()

    def change_annotation_fields(self, new_fields):
        self.annotationFields  = new_fields
        self.save()

class Image(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    imageId = models.AutoField(primary_key=True)
    file = models.ImageField(upload_to='images/', default='images/default.png')
    annotation = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Image {self.imageId} in {self.project.projectName}"

    def save(self, *args, **kwargs):
        # Call parent save method first to save the image itself
        super().save(*args, **kwargs)

        # After saving the image, update the annotations on the related project
        self.project.update_annotation_fields()
