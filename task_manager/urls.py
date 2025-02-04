from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger configuration
schema_view = get_schema_view(
    openapi.Info(
        title="Task Manager API",
        default_version='v1',
        description="API documentation for Task Manager",
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),  # Include the tasks app URLs
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Token obtain view
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Token refresh view
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Swagger API docs
]
