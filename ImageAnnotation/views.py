from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required



from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth import login as auth_login

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny
from django.contrib.auth.views import LoginView

from django.contrib.auth.models import User
from .models import Project, Image
from .serializers import ProjectSerializer, ImageSerializer

from django.utils.timezone import now
from django.contrib import messages
import os
import csv




@login_required
def get_user_data(request):
    user_data = {
        'username': request.user.username,
        'email': request.user.email
    }
    return JsonResponse(user_data)


def logout_view(request):
    logout(request)
    return redirect('login')
@csrf_exempt   
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'register.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('main')

    return render(request, 'register.html')

@login_required
def main_view(request):
    return render(request, 'main.html')


from django.db.models import Count
@api_view(['GET'])
@login_required
def get_projects(request):
    user = request.user  # Get the authenticated user
    # Annotate the number of images for each project
    projects = Project.objects.filter(user=user).annotate(num_images=Count('images'))
    
    # Serialize the projects, including the annotated field
    serialized_projects = ProjectSerializer(projects, many=True)
    print(serialized_projects)
    return Response(serialized_projects.data)
    






@api_view(['POST']) 
def create_new_project(request):
    project_name = request.data.get('projectName')
    project_description = request.data.get('projectDescription')
    images = request.FILES.getlist('images')


    if not project_name:
        return Response({'status': 400, 'message': 'Project name is required'}, status=400)

    try:
        # Create the project
        project = Project.objects.create(
            user=request.user,
            projectName=project_name,
            projectDescription=project_description or "",
            creation_date=now(),
            last_seen=now(),
            last_used=now()
        )
        for image in images:
            Image.objects.create(project=project, file=image, annotation = None)
        '''
        # Create the CSV file in the specified folder
        csv_file_path = os.path.join(image_folder, f"{project_name}_annotations.csv")
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Image Name', 'Annotation'])  # CSV headers
            writer.writerows(image_data)  # Write image data rows
        '''
        return Response({
            'status': 200,
            'message': 'Project created successfully',
            'project_id': project.projectId,
        })
    except Exception as e:
        return Response({'status': 400, 'message': f'Error creating project: {str(e)}'}, status=400)
    


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Project, Image

from django.views.generic.base import TemplateView

class ProjectPageView(TemplateView):
    template_name = 'project_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = kwargs.get('projectID')
        project = get_object_or_404(Project, projectId=project_id)
        project.last_seen = now()
        project.save()
        context['projectID'] = project_id
        return context


from django.core.paginator import Paginator
from .models import Project, Image
from .serializers import ProjectSerializer, ImageSerializer

from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Project, Image
from .serializers import ProjectSerializer, ImageSerializer

def load_project(request, projectID):
    # Fetch the project (ensures only one result)
    user = request.user
    project = get_object_or_404(Project.objects.annotate(num_images=Count('images')), user=user, projectId=projectID)

    project.last_seen = now()
    project.save()

    project.update_annotation_fields()
    
    # Serialize the project
    serialized_project = ProjectSerializer(project).data

    # Get the page number from the request (default to 1)
    page_number = request.GET.get('page', 1)
    
    # Get the label parameter from the request, if provided
    label = request.GET.get('label', None)

    # Fetch the images associated with the project
    images = Image.objects.filter(project=project)

    if label:
        if label == 'No Annotation':
            # Filter images that do not have an annotation (annotation is either null or empty)
            images = images.filter(annotation__isnull=True) | images.filter(annotation='')
        else:
            # Filter images by the specific annotation label
            images = images.filter(annotation=label)

    # Set up pagination (8 images per page)
    paginator = Paginator(images, 8)
    
    # Get the images for the current page
    page = paginator.get_page(page_number)
    
    # Serialize the images for the current page
    serialized_images = ImageSerializer(page.object_list, many=True).data

    # Return the project details with paginated images
    return JsonResponse({
        "username": user.username,
        "project_data": serialized_project,
        "images": serialized_images,
        "total_pages": paginator.num_pages,
        "current_page": page.number,
    })



from django.http import JsonResponse, FileResponse
from django.shortcuts import get_object_or_404

def fetch_image(request, image_id):
    # Fetch the image by ID
    image = get_object_or_404(Image, imageId=image_id)
    project = image.project

    # Update last_seen
    project.last_seen = now()
    project.save()
    # Get the full path of the image file
    file_path = image.file.path

    try:
        # Return the image file as a response without manually opening it
        response = FileResponse(open(file_path, 'rb'), content_type='image/jpeg')  # Adjust content type if necessary
        response['Content-Disposition'] = f'inline; filename="{image.file.name}"'
        return response
    except FileNotFoundError:
        return JsonResponse({"error": "File not found."}, status=404)


from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser

@api_view(['POST'])
@parser_classes([MultiPartParser])
def upload_files(request, projectID):
    """
    API endpoint to handle file and folder uploads.
    """
    files = request.FILES.getlist('images')
    if not files:
        return JsonResponse({'error': 'No files uploaded'}, status=400)
    
    user = request.user
    project = get_object_or_404(Project.objects.annotate(num_images=Count('images')), user=user, projectId=projectID)

    # Update last_seen and last_used
    project.last_seen = now()
    project.last_used = now()
    project.save()
    for file in files:
        # Save the file to the Image model
        Image.objects.create(project=project, file=file, annotation = None)

    return JsonResponse({'message': 'Files uploaded successfully'}, status=200)




import json
from django.http import JsonResponse

def update_labels(request, projectID):
    user = request.user
    try:
        # Fetch the project
        project = Project.objects.get(projectId=projectID)
            # Update last_seen and last_used
        project.last_seen = now()
        project.last_used = now()
        project.save()
    except Project.DoesNotExist:
        return JsonResponse({"status": "404", "message": "Project not found"}, status=404)

    # Ensure the request content type is JSON
    if request.content_type != 'application/json':
        return JsonResponse({"status": "400", "message": "Invalid content type. Expected application/json."}, status=400)

    # Get new annotations from the request (corrected for JSON)
    try:
        new_annotations = json.loads(request.body.decode('utf-8')).get('labels', [])
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"status": "400", "message": "Invalid JSON format."}, status=400)

    if not isinstance(new_annotations, list):
        return JsonResponse({"status": "400", "message": "Invalid labels format. Must be a list."}, status=400)

    # Calculate the annotations to be removed
    current_annotations = set(project.annotationFields)
    new_annotations_set = set([ann["label"] for ann in new_annotations if isinstance(ann, dict) and "label" in ann])
    annotation_difference = current_annotations - new_annotations_set

    alerts = []

    # Process annotations to be removed
    for ann in annotation_difference:
        
        if Image.objects.filter(annotation= ann).exists() == False:
            pass
        else:
            alerts.append({"label": ann})
            new_annotations_set.add(ann)

    # Update project annotations
    project.change_annotation_fields(list(new_annotations_set))

    # If there are alerts, return a conflict notification
    if alerts:
        return JsonResponse(
            {
                "status": "200",
                "message": "Cannot remove annotations in use without delete action",
                "conflicting_annotations": alerts
            },
            status=200
        )

    
    return JsonResponse({"status": "200", "message": "Annotations updated successfully"}, status=200)



def resolve_conflict(request, projectID):
    user = request.user
    try:
        # Fetch the project
        project = Project.objects.get(projectId=projectID)

        # Update last_seen and last_used
        project.last_seen = now()
        project.last_used = now()
        project.save()
    except Project.DoesNotExist:
        return JsonResponse({"status": "404", "message": "Project not found"}, status=404)

    # Ensure the request content type is JSON
    if request.content_type != 'application/json':
        return JsonResponse({"status": "400", "message": "Invalid content type. Expected application/json."}, status=400)
    
    try:
        conflicts = json.loads(request.body.decode('utf-8')).get('conflicts', [])
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"status": "400", "message": "Invalid JSON format."}, status=400)

    if not isinstance(conflicts, list):
        return JsonResponse({"status": "400", "message": "Invalid conflicts format. Must be a list."}, status=400)
    
    # Process each conflict
    for conflict in conflicts:
        label = conflict.get('label')
        if label:
            # Delete the annotation from all images that have it
            Image.objects.filter(annotation=label).update(annotation=None)
            project.annotationFields.remove(label)
            project.save()

    return JsonResponse({"status": "200", "message": "Labels updated successfully"}, status=200)


def get_annotatable_images(request, project_id):
    try:
        # Get the project based on the project_id
        project = get_object_or_404(Project, projectId=project_id)
        # Update last_seen
        project.last_seen = now()
        project.save()

        # Filter unannotated images
        unannotated_images = Image.objects.filter(project=project, annotation__isnull=True)

        # Prepare image data with the fetch_image URL
        image_data = [
            {
                'id': image.imageId,
                'file': reverse('get_image', args=[image.imageId])  # Generate the URL for fetching the image
            }
            for image in unannotated_images
        ]

        return JsonResponse({'images': image_data})
    except Project.DoesNotExist:
        return JsonResponse({'error': 'Project not found'}, status=404)
    
# Update annotation for an image
def update_annotation(request, image_id):
    try:
        image = Image.objects.get(id=image_id)
        annotation = request.POST.get('annotation')
        image.annotation = annotation
        image.save()
        return JsonResponse({"status": "success"})
    except Image.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Image not found"}, status=404)

# View for starting annotation
def annotation(request, project_id):

    return render(request, 'annotation.html')


def get_project_annotations(request, project_id):
    project = get_object_or_404(Project, projectId=project_id)
    return JsonResponse({'annotationFields': project.annotationFields})


def update_annotation(request, image_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            label = data.get('label') 
            if not label:
                return JsonResponse({'error': 'Label is required'}, status=400)

            image = Image.objects.get(imageId=image_id)
            image.annotation = label
            image.save()

            return JsonResponse({'message': 'Annotation updated successfully'})
        except Image.DoesNotExist:
            return JsonResponse({'error': 'Image not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def edit_project_name(request, project_id):
    if request.method == "POST":
        try:
            # Parse JSON request body
            body = json.loads(request.body)
            new_name = body.get("projectName", "")

            if not new_name:
                return JsonResponse({"error": "Project name cannot be empty"}, status=400)

            # Fetch the project and update its name
            project = get_object_or_404(Project, projectId=project_id)
            project.projectName = new_name
            project.save()

            return JsonResponse({"success": True, "projectName": project.projectName}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

def delete_project(request, project_id):
    if request.method == "DELETE":
        try:
            # Get the project by ID and delete it
            project = get_object_or_404(Project, projectId=project_id)
            project.delete()

            return JsonResponse({"success": True}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

from django.http import  HttpResponseNotAllowed
def delete_image(request, project_id, image_id):
    if request.method == 'DELETE':
        # Get the project and image
        project = get_object_or_404(Project, projectId=project_id)
        image = get_object_or_404(Image, imageId=image_id, project=project)
        
        # Delete the image file if it exists
        try:
            image.file.delete()  
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        # Delete the image record from the database
        image.delete()

        return JsonResponse({'success': 'Image deleted successfully'}, status=200)

    return HttpResponseNotAllowed(['DELETE'])


from django.http import HttpResponse, JsonResponse
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from zipfile import ZipFile
import os
import csv
import json
import tensorflow as tf  

def download_option(request, option, project_id):
    """
    Handles download requests based on the selected option.
    """
    if request.method == "GET":
        if option == 1:
            return save_to_folders(request, project_id)
        elif option == 2:
            return save_with_csv(request, project_id)
        elif option == 3:
            return save_with_json(request, project_id)
        elif option == 4:
            return save_as_tfrecord(request, project_id)
        else:
            return JsonResponse({"error": "Invalid option"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


def save_to_folders(request, project_id):
    project = get_object_or_404(Project, projectId=project_id)
    images = Image.objects.filter(project=project)

    if not images.exists():
        return HttpResponse("No images found for this project.", status=404)

    zip_filename = "labeled_images_folders.zip"

    # Create a zip file containing images grouped by label
    with ZipFile(zip_filename, 'w') as zipf:
        for image in images:
            label = image.annotation or "unlabeled"  # Use "unlabeled" if no annotation
            folder_path = f"{label}/"  # Create folder for each label
            filename = os.path.basename(image.file.path)
            zipf.write(image.file.path, arcname=os.path.join(folder_path, filename))

    # Open the zip file and prepare for the response
    with open(zip_filename, 'rb') as f:
        response = HttpResponse(f.read(), content_type="application/zip")
        response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'

    # Cleanup: Delete the zip file after sending the response
    try:
        os.remove(zip_filename)  # Remove the zip file
    except Exception as e:
        print(f"Error cleaning up file: {e}")

    return response


def save_with_csv(request, project_id):
    project = get_object_or_404(Project, projectId=project_id)
    images = Image.objects.filter(project = project)

    if not images.exists():
        return HttpResponse("No images found for this project.", status=404)

    zip_filename = "labeled_images_csv.zip"
    csv_filename = "labels.csv"

    with ZipFile(zip_filename, 'w') as zipf:
        # Add images
        for image in images:
            zipf.write(image.file.name, arcname=os.path.basename(image.file.name))

        # Add CSV
        csv_data = [("image", "label")]
        csv_data += [(os.path.basename(image.file.name), image.annotation or "unlabeled") for image in images]
        with open(csv_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(csv_data)
        zipf.write(csv_filename)

    # Serve the zip file
    with open(zip_filename, 'rb') as f:
        response = HttpResponse(f.read(), content_type="application/zip")
        response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'
        
    # Clean up after serving the file
    try:
        os.remove(zip_filename)  # Clean up zip file
        os.remove(csv_filename)  # Clean up csv file if any
    except Exception as e:
        print(f"Error cleaning up files: {e}")

    return response




def save_with_json(request, project_id):
    project = get_object_or_404(Project, projectId=project_id)
    images = Image.objects.filter(project=project)

    if not images.exists():
        return HttpResponse("No images found for this project.", status=404)

    zip_filename = "labeled_images_json.zip"
    json_filename = "annotations.json"

    # Create annotations data for the JSON
    annotations = [{"image": os.path.basename(image.file.name), "label": image.annotation or "unlabeled"} for image in images]

    # Write data to zip file
    with ZipFile(zip_filename, 'w') as zipf:
        # Add images to the zip file
        for image in images:
            zipf.write(image.file.path, arcname=os.path.basename(image.file.name))

        # Add annotations as a JSON file inside the zip
        with open(json_filename, 'w') as jsonfile:
            json.dump(annotations, jsonfile, indent=4)
        zipf.write(json_filename)

    # Serve the zip file as a response
    with open(zip_filename, 'rb') as f:
        response = HttpResponse(f.read(), content_type="application/zip")
        response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'

    # Cleanup: Ensure files are deleted after response is sent
    try:
        os.remove(zip_filename)  # Remove the zip file
        os.remove(json_filename)  # Remove the json file
    except Exception as e:
        print(f"Error cleaning up files: {e}")

    return response


def save_as_tfrecord(request, project_id):
    project = get_object_or_404(Project, projectId=project_id)
    images = Image.objects.filter(project=project)

    if not images.exists():
        return HttpResponse("No images found for this project.", status=404)

    tfrecord_filename = "labeled_images.tfrecord"
    zip_filename = "labeled_images_tfrecord.zip"

    # Create the TFRecord file
    with tf.io.TFRecordWriter(tfrecord_filename) as writer:
        for image in images:
            label = image.annotation or "unlabeled"
            image_data = open(image.file.path, 'rb').read()
            feature = {
                "image": tf.train.Feature(bytes_list=tf.train.BytesList(value=[image_data])),
                "label": tf.train.Feature(bytes_list=tf.train.BytesList(value=[label.encode()])),
            }
            example = tf.train.Example(features=tf.train.Features(feature=feature))
            writer.write(example.SerializeToString())

    # Zip the TFRecord file
    with ZipFile(zip_filename, 'w') as zipf:
        zipf.write(tfrecord_filename)

    # Open the zip file and prepare the response
    with open(zip_filename, 'rb') as f:
        response = HttpResponse(f.read(), content_type="application/zip")
        response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'

    # Clean up: Delete the files after serving the response
    try:
        os.remove(tfrecord_filename)  # Remove the TFRecord file
        os.remove(zip_filename)  # Remove the zip file
    except Exception as e:
        print(f"Error cleaning up files: {e}")

    return response