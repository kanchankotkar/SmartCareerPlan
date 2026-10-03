from rest_framework import serializers

from accounts.models import User
from careers.models import JobRole, JobRoleSkill
from skills.models import Skill
from learning.models import LearningResource


class AdminUserSerializer(serializers.ModelSerializer):

    target_role_name = serializers.CharField(
        source='target_role.role_name',
        read_only=True
    )

    class Meta:
        model = User
        fields = [
            'user_id',
            'full_name',
            'email',
            'education',
            'experience_years',
            'target_role',
            'target_role_name',
            'created_at'
        ]


class AdminJobRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobRole
        fields = [
            'role_id',
            'role_name',
            'description',
            'experience_level',
            'created_at'
        ]

        read_only_fields = [
            'role_id',
            'created_at'
        ]


class AdminJobRoleSkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobRoleSkill
        fields = [
            'role_skill_id',
            'role',
            'skill',
            'importance',
            'minimum_level'
        ]

        read_only_fields = [
            'role_skill_id'
        ]


class AdminLearningResourceSerializer(serializers.ModelSerializer):

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

        read_only_fields = [
            'resource_id',
            'created_at'
        ]