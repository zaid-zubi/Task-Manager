# Task Manager

A Django-based task management application with REST API endpoints for managing tasks. The application supports user authentication and provides both public and authenticated access to task data.

## Features

- User authentication with Basic Authentication
- CRUD operations for tasks
- Public and authenticated access to task data
- Swagger documentation for API endpoints
- Dockerized for easy deployment

## Installation

### Using Virtual Environment

1. Clone the repository:
    ```bash
    git clone https://github.com/zaid-zubi/Task-Manager
    cd task_manager
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Apply the migrations:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:
    ```bash
    python manage.py runserver
    ```

7. Access the admin dashboard:
    ```bash
    http://127.0.0.1:8000/admin/
    ```

### Using Docker

1. Clone the repository:
    ```bash
    git clone https://github.com/zaid-zubi/Task-Manager
    cd task_manager
    ```

2. Build and run the Docker containers:
    ```bash
    docker-compose up --build
    ```

3. Apply the migrations:
    ```bash
    docker-compose exec web python manage.py migrate
    ```

4. Create a superuser:
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

5. Access the application at `http://127.0.0.1:8000/`.

6. Access the admin dashboard:
    ```bash
    http://127.0.0.1:8000/admin/
    ```

## API Endpoints

### Task Endpoints

- `GET /api/tasks/` - Retrieve a list of tasks (Authenticated users only)
- `GET /api/tasks/{id}/` - Retrieve a single task (Public access)
- `POST /api/tasks/` - Create a new task (Authenticated users only)
- `PUT /api/tasks/{id}/` - Update an existing task (Authenticated users only)
- `DELETE /api/tasks/{id}/` - Delete a task (Authenticated users only)

## Usage

1. Access the admin panel at `http://127.0.0.1:8000/admin/` to manage users and tasks.
2. Use the provided API endpoints to interact with the task data.
3. Access the Swagger documentation at `http://127.0.0.1:8000/swagger/` for detailed API documentation.