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

    authentication_classes = [
        CustomJWTAuthentication
    ]

    def post(self, request):

        # First, check whether role_id was sent
        role_id = request.data.get("role_id")

        if role_id:
            role = JobRole.objects.filter(
                role_id=role_id
            ).first()
        else:
            # Use the target role already selected by the user
            role = request.user.target_role

        if not role:
            return Response(
                {
                    "error": "Please select a target job role first."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # --------------------------------
        # Skill level hierarchy
        # --------------------------------

        level_order = {
            "beginner": 1,
            "intermediate": 2,
            "advanced": 3
        }

        # --------------------------------
        # Get required skills
        # --------------------------------

        required_skills = JobRoleSkill.objects.filter(
            role=role
        ).select_related('skill')

        # --------------------------------
        # Get user's skills
        # --------------------------------

        user_skills = UserSkill.objects.filter(
            user=request.user
        ).select_related('skill')

        user_skill_levels = {}

        for user_skill in user_skills:

            skill_id = user_skill.skill.skill_id

            user_level = (
                user_skill.skill_level
                or "Beginner"
            ).lower()

            user_skill_levels[skill_id] = user_level

        # --------------------------------
        # Find skills needing learning
        # --------------------------------

        roadmap_skills = []

        for required in required_skills:

            skill_id = required.skill.skill_id

            required_level = (
                required.minimum_level
                or "Beginner"
            ).lower()

            # User doesn't have skill
            if skill_id not in user_skill_levels:

                roadmap_skills.append(
                    {
                        "skill": required.skill,
                        "reason": "Missing",
                        "current_level": None,
                        "required_level": (
                            required.minimum_level
                        )
                    }
                )

            else:

                user_level = user_skill_levels[
                    skill_id
                ]

                user_level_value = level_order.get(
                    user_level,
                    0
                )

                required_level_value = level_order.get(
                    required_level,
                    0
                )

                # User has skill but level is too low
                if user_level_value < required_level_value:

                    roadmap_skills.append(
                        {
                            "skill": required.skill,
                            "reason": "Below Required Level",
                            "current_level": (
                                user_level.title()
                            ),
                            "required_level": (
                                required.minimum_level
                            )
                        }
                    )

        # --------------------------------
        # Build roadmap
        # --------------------------------

        roadmap = []

        for item in roadmap_skills:

            skill = item["skill"]

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

                    "reason": item["reason"],

                    "current_level": (
                        item["current_level"]
                    ),

                    "required_level": (
                        item["required_level"]
                    ),

                    "resources": serializer.data
                }
            )

        return Response(
            {
                "role_id": role.role_id,
                "role_name": role.role_name,

                "total_learning_skills": (
                    len(roadmap_skills)
                ),

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
    