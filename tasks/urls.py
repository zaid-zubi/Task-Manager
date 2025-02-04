from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

# URLs for API Endpoints:
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('api/', include(router.urls)),

    path('create-task/', TaskViewSet.as_view({'get': 'task_form_page'}), name='task-form-page'),
    path('create-task/<int:task_id>/', TaskViewSet.as_view({'get': 'task_form_page'}), name='task-edit-page'),
    path('tasks/', TaskViewSet.as_view({'get': 'task_list_page'}), name='task-list-page'),
]