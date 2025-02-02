from rest_framework import serializers
from .models import Task

class TaskIn(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed', 'user']

from rest_framework.exceptions import ValidationError

def create(self, validated_data):
    user = self.context['request'].user
    if user is None or user.is_anonymous:
        raise ValidationError("Authentication credentials were not provided.")
    validated_data.pop('user', None)
    return Task.objects.create(user=user, **validated_data)
