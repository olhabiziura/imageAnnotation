
# Final Project: Dynamic Image Annotation Web Application

## Distinctiveness and Complexity

This web application is designed to allow users to annotate images with custom labels. It is distinct from other projects in the course, as it integrates complex functionalities such as image upload, dynamic label management, and real-time annotation editing. The project also utilizes a combination of Django for the backend (with models and views) and JavaScript for a responsive frontend, making it a robust and interactive web application.

The application allows users to upload images, annotate them with predefined or custom labels, and save those annotations. It also supports navigating between images and modifying annotations at any time. Additionally, it includes an image deletion feature to remove images from the dataset entirely. These features are handled through a combination of Django models (for storing image data and annotations) and JavaScript (for handling user interactions dynamically on the client side).

The project also ensures mobile responsiveness, providing an optimal user experience across different devices. The ability to add custom labels and interact with the annotations in a seamless, user-friendly interface adds complexity and makes the application stand out compared to simpler projects like social networks or e-commerce sites.

## Project Structure and File Overview

### Files and Directories

- **manage.py**: The Django project management script to run server, migrations, etc.
- **requirements.txt**: Contains a list of all Python packages and dependencies required to run the web application.
- **app_name/**: This is the main Django application folder, where all the application logic is housed.
    - **models.py**: Contains the Django models used to represent images and annotations in the database.
    - **views.py**: Contains views to handle HTTP requests for image uploading, annotation, and deletion, as well as returning dynamic content to the frontend.
    - **urls.py**: Defines the URL patterns for various routes like image uploading, annotation saving, and fetching image data.
    - **templates/**: Contains HTML files for rendering the pages, such as the home page with the image display and annotation form.
    - **static/**: Includes all static files such as JavaScript, CSS, and image assets.
        - **js/**: Contains JavaScript files to handle frontend interactions, such as adding labels and navigating between images.
        - **css/**: Includes the CSS files for styling the web application and making it mobile-responsive.
        
### Key Functionality

- **Image Upload and Display**: Users can upload images, and the images are displayed on the main page for annotation.
- **Dynamic Labeling**: Users can select from predefined labels or add custom labels. Labels can be clicked to apply them to images, and the selected label is saved dynamically.
- **Image Navigation**: Users can navigate through images with "Next" and "Previous" buttons, with annotations being saved as they progress through the images.
- **Delete Image**: Users can delete an image from the dataset by clicking on a red "X" button located at the top right corner of the image display area.
- **Mobile Responsiveness**: The layout is designed to adjust based on the screen size to ensure that the application is fully functional on mobile devices.

### How to Run the Application

1. Clone the repository to your local machine.
   
   ```bash
   git clone https://github.com/yourusername/project-repo.git
   cd project-repo
   ```

2. Install the required dependencies from the `requirements.txt` file.

   ```bash
   pip install -r requirements.txt
   ```

3. Apply database migrations.

   ```bash
   python manage.py migrate
   ```

4. Run the Django development server.

   ```bash
   python manage.py runserver
   ```

5. Open your browser and go to `http://127.0.0.1:8000/` to access the application.

### Additional Information

- **Features in Progress**: Some additional features that may be added later include user authentication (to allow different users to save their annotations separately), image cropping before annotation, and support for more advanced annotation types (such as bounding boxes or drawing).
  
- **Packages Used**: The project uses Django for backend development and jQuery for simplifying DOM manipulation. Additionally, JavaScript is used extensively for interactive elements like adding and selecting labels dynamically.

- **Database**: The application uses Django’s default SQLite database to store image data and annotations. However, you can configure it to use other database backends such as PostgreSQL or MySQL if needed.

## Conclusion

This project demonstrates the ability to design a dynamic, interactive web application with a combination of frontend and backend technologies. The use of Django and JavaScript together creates a responsive and seamless user experience, while the image annotation feature provides real-world utility. The project stands out by combining various technical elements into a cohesive application, and the mobile responsiveness ensures that it works well across all devices.

