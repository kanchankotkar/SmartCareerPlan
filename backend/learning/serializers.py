from rest_framework import serializers
from .models import LearningResource, LearningProgress


class LearningResourceSerializer(serializers.ModelSerializer):

    skill_name = serializers.CharField(
        source='skill.skill_name',
        read_only=True
    )

    class Meta:
        model = LearningResource
        fields = [
            'resource_id',
            'skill',
            'skill_name',
            'title',
            'description',
            'resource_type',
            'resource_url',
            'difficulty',
            'estimated_hours',
            'created_at'
        ]
class LearningProgressSerializer(serializers.ModelSerializer):

    resource_title = serializers.CharField(
        source='resource.title',
        read_only=True
    )

    class Meta:
        model = LearningProgress
        fields = [
            'progress_id',
            'resource',
            'resource_title',
            'progress_percentage',
            'status',
            'started_at',
            'completed_at'
        ]

        read_only_fields = [
            'progress_id',
            'started_at',
            'completed_at'
        ]        