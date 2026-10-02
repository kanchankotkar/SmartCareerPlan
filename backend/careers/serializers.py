from rest_framework import serializers

from .models import JobRole, JobRoleSkill


class JobRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobRole
        fields = [
            'role_id',
            'role_name',
            'description',
            'experience_level',
            'created_at'
        ]


class JobRoleSkillSerializer(serializers.ModelSerializer):

    skill_name = serializers.CharField(
        source='skill.skill_name',
        read_only=True
    )

    category = serializers.CharField(
        source='skill.category',
        read_only=True
    )

    class Meta:
        model = JobRoleSkill
        fields = [
            'role_skill_id',
            'skill',
            'skill_name',
            'category',
            'importance',
            'minimum_level'
        ]