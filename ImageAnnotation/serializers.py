from rest_framework import serializers
from .models import Project, Image

class ProjectSerializer(serializers.ModelSerializer):
    num_images = serializers.IntegerField(read_only=True)  # Define the annotated field explicitly

    class Meta:
        model = Project
        fields = ['projectId', 'projectName', 'projectDescription','annotationFields', 'num_images'] 

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['imageId', 'file', 'annotation']
