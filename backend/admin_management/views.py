from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.authentication import CustomJWTAuthentication
from accounts.models import User

from careers.models import JobRole, JobRoleSkill

from skills.models import Skill

from learning.models import LearningResource

from .serializers import (
    AdminUserSerializer,
    AdminJobRoleSerializer,
    AdminLearningResourceSerializer
)

from .permissions import IsAdminUser


class AdminUserListView(APIView):

    authentication_classes = [
        CustomJWTAuthentication
    ]

    permission_classes = [
        IsAdminUser
    ]

    def get(self, request):

        users = User.objects.select_related(
            'target_role'
        ).all()

        serializer = AdminUserSerializer(
            users,
            many=True
        )

        return Response(
            {
                "total_users": users.count(),
                "users": serializer.data
            },
            status=status.HTTP_200_OK
        )


class AdminJobRoleCreateView(APIView):

    authentication_classes = [
        CustomJWTAuthentication
    ]

    permission_classes = [
        IsAdminUser
    ]

    def post(self, request):

        serializer = AdminJobRoleSerializer(
            data=request.data
        )

        if serializer.is_valid():

            job_role = serializer.save()

            return Response(
                {
                    "message": "Job role created successfully",
                    "job_role": AdminJobRoleSerializer(
                        job_role
                    ).data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class AdminJobRoleSkillCreateView(APIView):

    authentication_classes = [
        CustomJWTAuthentication
    ]

    permission_classes = [
        IsAdminUser
    ]

    def post(self, request):

        role_id = request.data.get('role')
        skill_id = request.data.get('skill')

        if not role_id:
            return Response(
                {
                    "error": "role is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not skill_id:
            return Response(
                {
                    "error": "skill is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        role = JobRole.objects.filter(
            role_id=role_id
        ).first()

        if not role:
            return Response(
                {
                    "error": "Job role not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        skill = Skill.objects.filter(
            skill_id=skill_id
        ).first()

        if not skill:
            return Response(
                {
                    "error": "Skill not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        existing = JobRoleSkill.objects.filter(
            role=role,
            skill=skill
        ).first()

        if existing:
            return Response(
                {
                    "error": "This skill is already assigned to this job role."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        job_role_skill = JobRoleSkill.objects.create(
            role=role,
            skill=skill,
            importance=request.data.get(
                'importance',
                'Required'
            ),
            minimum_level=request.data.get(
                'minimum_level',
                'Beginner'
            )
        )

        return Response(
            {
                "message": "Skill assigned to job role successfully",
                "job_role_skill": {
                    "role_skill_id": job_role_skill.role_skill_id,
                    "role_id": role.role_id,
                    "role_name": role.role_name,
                    "skill_id": skill.skill_id,
                    "skill_name": skill.skill_name,
                    "importance": job_role_skill.importance,
                    "minimum_level": job_role_skill.minimum_level
                }
            },
            status=status.HTTP_201_CREATED
        )

class AdminLearningResourceCreateView(APIView):

    authentication_classes = [
        CustomJWTAuthentication
    ]

    permission_classes = [
        IsAdminUser
    ]

    def post(self, request):

        skill_id = request.data.get('skill')

        if not skill_id:
            return Response(
                {
                    "error": "skill is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        skill = Skill.objects.filter(
            skill_id=skill_id
        ).first()

        if not skill:
            return Response(
                {
                    "error": "Skill not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AdminLearningResourceSerializer(
            data=request.data
        )

        if serializer.is_valid():

            resource = serializer.save()

            return Response(
                {
                    "message": "Learning resource created successfully",

                    "resource": {
                        "resource_id": resource.resource_id,
                        "skill_id": skill.skill_id,
                        "skill_name": skill.skill_name,
                        "title": resource.title,
                        "description": resource.description,
                        "resource_type": resource.resource_type,
                        "resource_url": resource.resource_url,
                        "difficulty": resource.difficulty,
                        "estimated_hours": resource.estimated_hours
                    }
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )    