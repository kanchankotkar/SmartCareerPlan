from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.authentication import CustomJWTAuthentication
from skills.models import UserSkill
from careers.models import JobRole, JobRoleSkill

from django.utils import timezone

from .models import LearningResource, LearningProgress
from .serializers import (
    LearningResourceSerializer,
    LearningProgressSerializer
)


class LearningRoadmapView(APIView):

    authentication_classes = [CustomJWTAuthentication]

    def post(self, request):

        role_id = request.data.get('role_id')

        if not role_id:
            return Response(
                {
                    "error": "role_id is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Find job role
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

        # Get required skills for the role
        required_skills = JobRoleSkill.objects.filter(
            role=role
        ).select_related('skill')

        # Get user's skills
        user_skills = UserSkill.objects.filter(
            user=request.user
        ).select_related('skill')

        # Convert user skills into skill IDs
        user_skill_ids = {
            user_skill.skill.skill_id
            for user_skill in user_skills
        }

        # Find missing skills
        missing_skills = []

        for required in required_skills:

            if required.skill.skill_id not in user_skill_ids:

                missing_skills.append(
                    required.skill
                )

        # Find learning resources
        roadmap = []

        for skill in missing_skills:

            resources = LearningResource.objects.filter(
                skill=skill
            )

            serializer = LearningResourceSerializer(
                resources,
                many=True
            )

            roadmap.append(
                {
                    "skill_id": skill.skill_id,
                    "skill_name": skill.skill_name,
                    "category": skill.category,
                    "resources": serializer.data
                }
            )

        return Response(
            {
                "role_id": role.role_id,
                "role_name": role.role_name,
                "total_missing_skills": len(missing_skills),
                "learning_roadmap": roadmap
            },
            status=status.HTTP_200_OK
        )

class LearningProgressView(APIView):

    authentication_classes = [CustomJWTAuthentication]

    def post(self, request):

        resource_id = request.data.get('resource_id')
        progress_percentage = request.data.get(
            'progress_percentage'
        )

        if resource_id is None:
            return Response(
                {
                    "error": "resource_id is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if progress_percentage is None:
            return Response(
                {
                    "error": "progress_percentage is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Convert progress to number
        try:
            progress_percentage = float(
                progress_percentage
            )
        except ValueError:
            return Response(
                {
                    "error": "progress_percentage must be a number"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate progress range
        if progress_percentage < 0 or progress_percentage > 100:
            return Response(
                {
                    "error": "Progress must be between 0 and 100"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check resource
        resource = LearningResource.objects.filter(
            resource_id=resource_id
        ).first()

        if not resource:
            return Response(
                {
                    "error": "Learning resource not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Determine status
        if progress_percentage == 0:
            status_value = "Not Started"

        elif progress_percentage == 100:
            status_value = "Completed"

        else:
            status_value = "In Progress"

        # Check existing progress
        progress = LearningProgress.objects.filter(
            user=request.user,
            resource=resource
        ).first()

        if progress:

            progress.progress_percentage = progress_percentage
            progress.status = status_value

            if progress_percentage > 0 and not progress.started_at:
                progress.started_at = timezone.now()

            if progress_percentage == 100:
                progress.completed_at = timezone.now()

            progress.save()

            message = "Progress updated successfully"

        else:

            progress = LearningProgress.objects.create(
                user=request.user,
                resource=resource,
                progress_percentage=progress_percentage,
                status=status_value,
                started_at=(
                    timezone.now()
                    if progress_percentage > 0
                    else None
                ),
                completed_at=(
                    timezone.now()
                    if progress_percentage == 100
                    else None
                )
            )

            message = "Progress added successfully"

        serializer = LearningProgressSerializer(
            progress
        )

        return Response(
            {
                "message": message,
                "progress": serializer.data
            },
            status=status.HTTP_200_OK
        )

    def get(self, request):

        progress_records = LearningProgress.objects.filter(
            user=request.user
        ).select_related('resource')

        serializer = LearningProgressSerializer(
            progress_records,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    