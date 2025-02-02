from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import Task
from .serializers import TaskIn

class TaskViewSet(ViewSet):
    
    def list(self, request):
        """List all tasks for the authenticated user."""
        if request.user.is_authenticated:
            tasks = Task.objects.filter(user=request.user)
            serializer = TaskIn(tasks, many=True)
            return Response(serializer.data)
        return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
    
    def retrieve(self, request, pk=None):
        """Retrieve a single task for any user."""
        task = get_object_or_404(Task, id=pk)
        serializer = TaskIn(task)
        return Response(serializer.data)

    def create(self, request):
        """Create a new task for the authenticated user."""
        if request.user.is_authenticated:
            serializer = TaskIn(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, pk=None):
        """Update an existing task for the authenticated user."""
        if request.user.is_authenticated:
            task = get_object_or_404(Task, id=pk, user=request.user)
            serializer = TaskIn(instance=task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, pk=None):
        """Delete a task for the authenticated user."""
        if request.user.is_authenticated:
            task = get_object_or_404(Task, id=pk, user=request.user)
            task.delete()
            return Response({"message": "Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
