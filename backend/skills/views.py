from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.authentication import CustomJWTAuthentication

from .models import Skill, UserSkill
from .serializers import SkillSerializer, UserSkillSerializer


class SkillListView(APIView):

    def get(self, request):

        skills = Skill.objects.all()

        serializer = SkillSerializer(
            skills,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

class AddUserSkillView(APIView):

    authentication_classes = [CustomJWTAuthentication]

    def post(self, request):

        serializer = UserSkillSerializer(
            data=request.data
        )

        if serializer.is_valid():

            skill = serializer.validated_data['skill']

            # Check whether user already has this skill
            existing_skill = UserSkill.objects.filter(
                user=request.user,
                skill=skill
            ).first()

            if existing_skill:

                return Response(
                    {
                        "error": "You already have this skill."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            user_skill = serializer.save(
                user=request.user
            )

            return Response(
                {
                    "message": "Skill added successfully",
                    "user_skill_id": user_skill.user_skill_id,
                    "skill": user_skill.skill.skill_name,
                    "skill_level": user_skill.skill_level,
                    "years_experience": user_skill.years_experience
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class MySkillsView(APIView):

    authentication_classes = [CustomJWTAuthentication]

    def get(self, request):

        user_skills = UserSkill.objects.filter(
            user=request.user
        ).select_related('skill')

        data = []

        for user_skill in user_skills:

            data.append(
                {
                    "user_skill_id": user_skill.user_skill_id,
                    "skill_id": user_skill.skill.skill_id,
                    "skill_name": user_skill.skill.skill_name,
                    "category": user_skill.skill.category,
                    "skill_level": user_skill.skill_level,
                    "years_experience": user_skill.years_experience,
                    "is_verified": user_skill.is_verified
                }
            )

        return Response(
            data,
            status=status.HTTP_200_OK
        )        