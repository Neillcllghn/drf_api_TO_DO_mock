from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from django.utils import timezone
from .models import Task, Category


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    due_date = serializers.DateField(required=False)
    updated_at = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs['context']['request']
        user = request.user
        super(TaskSerializer, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(owner=user)

    def validate(self, data):
        if self.instance is None and data['due_date'] < timezone.now().date():
            raise serializers.ValidationError("The date cannot be in the past when creating a task!")
        return data

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_updated_at(self, obj):
        return naturaltime(obj.updated_at)

    class Meta:
        model = Task
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'category', 'title',
            'description', 'is_urgent', 'due_date', 'completed', 'is_owner',
            'profile_id', 'profile_image',
        ]


class TaskDetailSerializer(TaskSerializer):
    category = serializers.ReadOnlyField(source='category.id')


    # def validate_category(self, value):
    #     user = self.context['request'].user
    #     if value.owner != user:
    #         raise serializers.ValidationError(
    #     "You do not have permission - you need to create your own category"
    #     )
    #     return value

