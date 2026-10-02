from rest_framework import serializers

from .models import Skill,UserSkill


class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = [
            'skill_id',
            'skill_name',
            'category',
            'description',
            'created_at'
        ]

class UserSkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSkill
        fields = [
            'user_skill_id',
            'skill',
            'skill_level',
            'years_experience',
            'is_verified',
            'added_at'
        ]
        read_only_fields = [
            'user_skill_id',
            'is_verified',
            'added_at'
        ]
