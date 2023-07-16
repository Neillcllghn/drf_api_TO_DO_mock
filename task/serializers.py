from rest_framework import serializers
from django.utils import timezone
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    due_date = serializers.DateField(required=False,
            input_formats=["%Y-%m-%d"]
            )
    
    def validate(self, data):
        if data['due_date'] < timezone.now().date():
            raise serializers.ValidationError("The date cannot be in the past!")
        return data   

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    # def validate_category(self, value):
    #     user = self.context['request'].user
    #     if value.owner != user:
    #         raise serializers.ValidationError(
    #     "You do not have permission - you need to create your own category"
    #     )
    #     return value

    class Meta:
        model = Task
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'category', 'title',
            'description', 'is_urgent', 'due_date', 'completed', 'is_owner',
        ]

class TaskDetailSerializer(TaskSerializer):
    category = serializers.ReadOnlyField(source='category.id')
