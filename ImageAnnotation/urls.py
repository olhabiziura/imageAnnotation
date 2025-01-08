"""ImageAnnotation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from rest_framework.authtoken.views import obtain_auth_token
from . import views  # Assuming you have custom views for registration

urlpatterns = [
    path('admin/', admin.site.urls),

    path("logout", views.logout_view, name="logout"),

    path('', TemplateView.as_view(template_name='login.html'), name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('main/', views.main_view, name='main'),
    path('logout/', views.logout_view, name='logout'),
    path('user/', views.get_user_data, name='get_user_data'),

    path('start-annotating/<int:project_id>/', views.annotation, name='start_annotation'),
    path('continue-annotating/<int:project_id>/', views.annotation, name='continue_annotation'),
    
    # For saving an annotation for an image
    path('update-annotation/<int:image_id>/', views.update_annotation, name='update_annotation'),
    path('<int:project_id>/get-annotatable-images/', views.get_annotatable_images),

    path('projects/', views.get_projects, name = 'projects'),
    path('create_project/', TemplateView.as_view(template_name='create.html'), name='create_project'),
    path('create_project/submit/', views.create_new_project, name='create_new_project'),
    path('<int:projectID>/', views.load_project, name='project_page'),
    path('<int:project_id>/edit/', views.edit_project_name, name='edit_project_name'),
    path('<int:project_id>/delete/', views.delete_project, name='delete_project'),

    path('<int:projectID>/display/', TemplateView.as_view(template_name='project_page.html'), name='project_page'),

    path('image/<int:image_id>/', views.fetch_image, name = 'get_image'),
    path('<int:projectID>/upload-images/', views.upload_files, name='upload_images'),
    path('projects/<int:project_id>/delete-image/<int:image_id>/', views.delete_image, name='delete_image'),
    path('<int:projectID>/update-labels/', views.update_labels, name='update_labels'),
    path('<int:projectID>/resolve-conflicts/', views.resolve_conflict, name='resolve_conflict'),
    path('projects/<int:project_id>/get-annotations/', views.get_project_annotations, name='get_project_annotations'),
    path('update-annotation/<int:image_id>/', views.update_annotation, name='update_annotation'),
    path('download/<int:project_id>/<int:option>/', views.download_option, name='download_option'),



]
