# ImageAnnotation

ImageAnnotation is a comprehensive tool designed to simplify and enhance the process of labeling and annotating images for use in machine learning models and data analysis. This project provides an intuitive, efficient interface for managing large-scale annotation tasks, enabling seamless integration into AI pipelines.

---

## Features

- **User-Friendly Interface**: Quickly and efficiently annotate images with tools for bounding boxes( to be implemented ), polygons, or key points.
- **Customizable Annotation Categories**: Tailor categories to fit specific project requirements.
- **Batch Upload and Management**: Upload multiple images at once and manage them with ease.
- **Real-Time Annotation Rendering**: Instant feedback on your annotations, improving productivity.
- **Export Annotations**: Supports popular formats such as COCO JSON, Pascal VOC, and CSV for easy integration into machine learning workflows.
- **Multi-Device Compatibility**: Designed for desktops, tablets, and mobile devices, ensuring flexibility and ease of use.

---

## Technologies Used

- **Backend**:
  - Django (Python): Provides a robust framework for the application’s logic and database management.
- **Frontend**:
  - JavaScript: Ensures dynamic interactivity for users.
  - HTML and CSS: For creating responsive and visually appealing layouts.
  - Bootstrap: Streamlines UI design with pre-built components.
- **Database**:
  - SQLite: Default database, easily extendable to PostgreSQL or MySQL for production environments.
- **Others**:
  - RESTful APIs: Enable smooth communication between the frontend and backend.
  - Webpack: Bundles frontend assets for optimized performance.

---

## Installation

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual Environment tool (optional but recommended)

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/olhabiziura/imageAnnotation.git
   ```

2. **Navigate to the Project Directory**

   ```bash
   cd imageAnnotation
   ```

3. **Set Up a Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Apply Database Migrations**

   ```bash
   python manage.py migrate
   ```

6. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```

7. **Access the Application**
   Open your browser and go to `http://127.0.0.1:8000`.

---

## Usage

### Annotating Images

1. **Upload Images**:
   - Use the upload interface to add images to your project.
2. **Select and Annotate**:
   - Choose an image and use the annotation tools to create bounding boxes, polygons, or key points.
3. **Assign Labels**:
   - Categorize annotations using predefined or custom labels.
4. **Save Progress**:
   - Save your work periodically to ensure no annotations are lost.
5. **Export Annotations**:
   - Export your annotations in COCO JSON, Pascal VOC, or CSV formats.

### Collaborative Workflow ( to be implemented ) 

- Invite team members to collaborate on a project.
- Use role-based permissions to manage access.

---

## Contribution

Contributions are welcome! To contribute:

1. **Fork the Repository**
   - Click the "Fork" button on GitHub.
2. **Create a New Branch**
   ```bash
   git checkout -b feature/your-feature
   ```
3. **Make Changes**
   - Implement your feature or fix.
4. **Commit Changes**
   ```bash
   git commit -m "Add feature: your feature"
   ```
5. **Push Changes to Your Fork**
   ```bash
   git push origin feature/your-feature
   ```
6. **Open a Pull Request**
   - Submit your changes for review.


---


## Author

[Olha Biziura](https://github.com/olhabiziura)

Feel free to reach out for questions, feedback, or collaboration ideas!

