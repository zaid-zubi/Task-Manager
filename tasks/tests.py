from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from tasks.models import Task
from tasks.serializers import TaskIn

class TaskViewSetTestCase(APITestCase):
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.task1 = Task.objects.create(user=self.user, title="Task 1", description="First task")
        self.task2 = Task.objects.create(user=self.user, title="Task 2", description="Second task")

        self.url = "/api/tasks/"

    def test_list_tasks_authenticated(self):
        """Test retrieving tasks with authentication"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        
        print(f"Generated Token: {self.access_token}")

        response = self.client.get(self.url)

        print(f"Response Status: {response.status_code}")
        print(f"Response Data: {response.data}")

        tasks = Task.objects.filter(user=self.user)
        serializer = TaskIn(tasks, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_list_tasks_unauthenticated(self):
        """Test retrieving tasks without authentication"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
