from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ViewSet
from drf_yasg.utils import swagger_auto_schema

from tasks.core.response import http_error_response, http_response
from .models import Task
from .serializers import TaskIn, TaskOut

class TaskViewSet(ViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """Retrieve a list of tasks (Authenticated users only)"""
        tasks = Task.objects.filter(user=request.user)
        serializer = TaskOut(tasks, many=True)
        return http_response(data=serializer.data, status_code=status.HTTP_200_OK, message="Tasks retrieved successfully")

    def retrieve(self, request, pk=None):
        """Retrieve a single task (Public access)"""
        try:
            task = Task.objects.get(id=pk, user=request.user)
        except Task.DoesNotExist as e:
            raise http_error_response(errors=str(e), status_code=status.HTTP_404_NOT_FOUND, message="Task not found")
        serializer = TaskOut(instance=task)
        return http_response(data=serializer.data, status_code=status.HTTP_200_OK, message="Task retrieved successfully")

    @swagger_auto_schema(request_body=TaskIn)
    def create(self, request):
        """Create a task (Authenticated users only)"""
        serializer = TaskIn(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Ensure task is linked to user
            return http_response(data=serializer.data, status_code=status.HTTP_201_CREATED, message="Task created successfully")
        return http_error_response(errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST, message="Invalid data")

    @swagger_auto_schema(request_body=TaskIn)
    def update(self, request, pk=None):
        """Update a task (Authenticated users only)"""
        try:
            task = Task.objects.get(id=pk, user=request.user)
        except Task.DoesNotExist as e:
            raise http_error_response(errors=str(e), status_code=status.HTTP_404_NOT_FOUND, message="Task not found")
        serializer = TaskIn(instance=task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return http_response(data=serializer.data, status_code=status.HTTP_201_CREATED, message="Task updated successfully")
        return http_error_response(errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST, message="Invalid data")

    def destroy(self, request, pk=None):
        """Delete a task (Authenticated users only)"""
        try:
            task = Task.objects.get(id=pk, user=request.user)
        except Task.DoesNotExist as e:
            raise http_error_response(errors=str(e), status_code=status.HTTP_404_NOT_FOUND, message="Task not found")
        task.delete()
        return http_response(data=None, status_code=status.HTTP_204_NO_CONTENT, message="Task deleted successfully")

    def task_form_page(self, request, task_id=None):
        """
        Render the task form page for creating/editing a task.
        Users can only edit tasks they created.
        """
        task = None
        if task_id:
            try:
                task = Task.objects.get(id=task_id, user=request.user)
            except Task.DoesNotExist as e:
                raise http_error_response(errors=str(e), status_code=status.HTTP_404_NOT_FOUND, message="Task not found")

        if request.method == "POST":
            form = TaskIn(request.POST, instance=task)
            if form.is_valid():
                form.save(user=request.user)  # Ensure task is linked to user
                return redirect('task-list-page')  # Redirect to task list page after saving
        else:
            form = TaskIn(instance=task)

        return render(request, 'task_form.html', {'form': form, 'task': task})

    def task_list_page(self, request):
        """Render the task list page (Authenticated users only)"""
        response = self.list(request=request)
        tasks = response.data
        return render(request, 'task_list.html', {'tasks': tasks.get("data")})

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def public_task_list(self, request):
        """
        Endpoint to get a list of all tasks (Public access).
        """
        tasks = Task.objects.all()
        serializer = TaskIn(tasks, many=True)
        return http_response(data=serializer.data, status_code=status.HTTP_200_OK, message="Tasks retrieved successfully")
