from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

# URLs for API Endpoints:
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    # API Endpoints (Handled by ViewSet)
    path('api/', include(router.urls)),  # Grouping all task-related endpoints

    # HTML Pages (Not part of API but accessible for authenticated users)
    path('create-task/', TaskViewSet.as_view({'get': 'task_form_page'}), name='task-form-page'),  # Create task form
    path('create-task/<int:task_id>/', TaskViewSet.as_view({'get': 'task_form_page'}), name='task-edit-page'),  # Edit task form
    path('tasks/', TaskViewSet.as_view({'get': 'task_list_page'}), name='task-list-page'),  # Task list page
]
