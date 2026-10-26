
from rest_framework import serializers

from .models import Skill, UserSkill


class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = [
            "skill_id",
            "skill_name",
            "category",
            "description",
            "created_at",
        ]


class UserSkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSkill
        fields = [
            "user_skill_id",
            "skill",
            "skill_level",
            "years_experience",
            "is_verified",
            "added_at",
        ]
        read_only_fields = [
            "user_skill_id",
            "is_verified",
            "added_at",
        ]

    def validate_skill_level(self, value):
        allowed_levels = [
            "Beginner",
            "Intermediate",
            "Advanced",
        ]

        if not value or value.strip() not in allowed_levels:
            raise serializers.ValidationError(
                "Choose Beginner, Intermediate, or Advanced."
            )

        return value.strip()

    def validate_years_experience(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError(
                "Years of experience cannot be negative."
            )

        return value
