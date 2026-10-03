from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.authentication import CustomJWTAuthentication
from skills.models import UserSkill

from .models import JobRole, JobRoleSkill
from .serializers import (
    JobRoleSerializer,
    JobRoleSkillSerializer
)


class JobRoleListView(APIView):

    def get(self, request):

        roles = JobRole.objects.all()

        serializer = JobRoleSerializer(
            roles,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class RequiredSkillsView(APIView):

    def get(self, request, role_id):

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

        role_skills = JobRoleSkill.objects.filter(
            role=role
        ).select_related('skill')

        serializer = JobRoleSkillSerializer(
            role_skills,
            many=True
        )

        return Response(
            {
                "role_id": role.role_id,
                "role_name": role.role_name,
                "required_skills": serializer.data
            },
            status=status.HTTP_200_OK
        )


class SkillGapAnalysisView(APIView):

    authentication_classes = [
        CustomJWTAuthentication
    ]

    def post(self, request):

        print("NEW SKILL GAP API IS RUNNING")

        role_id = request.data.get('role_id')

        if not role_id:

            return Response(
                {
                    "error": "role_id is required"
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

        required_skills = JobRoleSkill.objects.filter(
            role=role
        ).select_related('skill')

        user_skills = UserSkill.objects.filter(
            user=request.user
        ).select_related('skill')

        # --------------------------------
        # Skill Level Hierarchy
        # --------------------------------

        level_order = {
            "beginner": 1,
            "intermediate": 2,
            "advanced": 3
        }

        # --------------------------------
        # Store user's skills
        # --------------------------------

        user_skill_levels = {}

        for user_skill in user_skills:

            skill_name = (
                user_skill.skill.skill_name.lower()
            )

            user_level = (
                user_skill.skill_level
                or "Beginner"
            ).lower()

            user_skill_levels[skill_name] = {
                "level": user_level,
                "display_level": user_skill.skill_level
            }

        # --------------------------------
        # Compare skills
        # --------------------------------

        matched_skills = []

        below_required_skills = []

        missing_skills = []

        for required in required_skills:

            skill_name = (
                required.skill.skill_name.lower()
            )

            required_level = (
                required.minimum_level
                or "Beginner"
            ).lower()

            # User doesn't have the skill
            if skill_name not in user_skill_levels:

                missing_skills.append(
                    {
                        "skill": required.skill.skill_name,
                        "required_level": (
                            required.minimum_level
                        )
                    }
                )

            else:

                user_level = user_skill_levels[
                    skill_name
                ]["level"]

                user_display_level = user_skill_levels[
                    skill_name
                ]["display_level"]

                user_level_value = level_order.get(
                    user_level,
                    0
                )

                required_level_value = level_order.get(
                    required_level,
                    0
                )

                # User meets required level
                if user_level_value >= required_level_value:

                    matched_skills.append(
                        {
                            "skill": required.skill.skill_name,
                            "required_level": (
                                required.minimum_level
                            ),
                            "user_level": (
                                user_display_level
                            )
                        }
                    )

                # User has skill but level is too low
                else:

                    below_required_skills.append(
                        {
                            "skill": required.skill.skill_name,
                            "required_level": (
                                required.minimum_level
                            ),
                            "user_level": (
                                user_display_level
                            )
                        }
                    )

        # --------------------------------
        # Readiness calculation
        # --------------------------------

        total_required = required_skills.count()

        matched_count = len(matched_skills)

        if total_required > 0:

            readiness = (
                matched_count
                / total_required
            ) * 100

        else:

            readiness = 0

        # --------------------------------
        # Response
        # --------------------------------

        return Response(
            {
                "role_id": role.role_id,

                "role_name": role.role_name,

                "total_required_skills": (
                    total_required
                ),

                "matched_skills": (
                    matched_skills
                ),

                "below_required_level": (
                    below_required_skills
                ),

                "missing_skills": (
                    missing_skills
                ),

                "readiness_percentage": round(
                    readiness,
                    2
                )
            },

            status=status.HTTP_200_OK
        )