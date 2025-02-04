from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .serializers import TaskIn
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

class TaskViewSet(ViewSet):
    """
    Task API:
    - POST /api/tasks/ → Create a task (Authenticated users only)
    - GET /api/tasks/ → List all tasks (Authenticated users only)
    - GET /api/tasks/{id}/ → Retrieve a task (Public)
    - PUT /api/tasks/{id}/ → Update a task (Authenticated users only)
    - DELETE /api/tasks/{id}/ → Delete a task (Authenticated users only)
    """
    permission_classes = [IsAuthenticated]  # Default for all actions

    def list(self, request):
        """Retrieve a list of tasks (Authenticated users only)"""
        tasks = Task.objects.filter(user=request.user)
        serializer = TaskIn(tasks, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """Retrieve a single task (Public access)"""
        task = get_object_or_404(Task, id=pk)
        serializer = TaskIn(instance=task)
        return Response(serializer.data)
    
    @swagger_auto_schema(request_body=TaskIn)
    def create(self, request):
        """Create a task (Authenticated users only)"""
        serializer = TaskIn(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Ensure task is linked to user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(request_body=TaskIn)
    def update(self, request, pk=None):
        """Update a task (Authenticated users only)"""
        task = get_object_or_404(Task, id=pk, user=request.user)
        serializer = TaskIn(instance=task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Delete a task (Authenticated users only)"""
        task = get_object_or_404(Task, id=pk, user=request.user)
        task.delete()
        return Response({"message": "Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    def task_form_page(self, request, task_id=None):
        """Render the task form page for creating/editing a task"""
        task = None
        if task_id:
            task = get_object_or_404(Task, id=task_id, user=request.user)  # Only task owner can edit

        if request.method == "POST":
            # Handle form submission for both creating and updating tasks
            form = TaskIn(request.POST, instance=task)
            if form.is_valid():
                form.save(user=request.user)
                return redirect('task-list-page')  # Redirect to task list page after saving
        else:
            form = TaskIn(instance=task)

        return render(request, 'task_form.html', {'form': form, 'task': task})
    
    def task_list_page(self, request):
        """Render the task list page (Authenticated users only)"""
        response = self.list(request=request)
        tasks = response.data        
        return render(request, 'task_list.html', {'tasks': tasks})
