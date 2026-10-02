from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import JobRole, JobRoleSkill
from .serializers import (
    JobRoleSerializer,
    JobRoleSkillSerializer
)

from accounts.authentication import CustomJWTAuthentication
from skills.models import UserSkill

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

        # --------------------------------
        # 1. Find the selected job role
        # --------------------------------

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

        # --------------------------------
        # 2. Get required skills
        # --------------------------------

        required_skills = JobRoleSkill.objects.filter(
            role=role
        ).select_related('skill')

        # --------------------------------
        # 3. Get user's skills
        # --------------------------------

        user_skills = UserSkill.objects.filter(
            user=request.user
        ).select_related('skill')

        # --------------------------------
        # 4. Create skill name sets
        # --------------------------------

        required_skill_names = {
            item.skill.skill_name.lower()
            for item in required_skills
        }

        user_skill_names = {
            item.skill.skill_name.lower()
            for item in user_skills
        }

        # --------------------------------
        # 5. Find matched skills
        # --------------------------------

        matched_skills = (
            required_skill_names
            .intersection(user_skill_names)
        )

        # --------------------------------
        # 6. Find missing skills
        # --------------------------------

        missing_skills = (
            required_skill_names
            - user_skill_names
        )

        # --------------------------------
        # 7. Calculate readiness
        # --------------------------------

        total_required = len(
            required_skill_names
        )

        if total_required > 0:

            readiness = (
                len(matched_skills)
                / total_required
            ) * 100

        else:

            readiness = 0

        return Response(
            {
                "role_id": role.role_id,
                "role_name": role.role_name,

                "total_required_skills":
                    total_required,

                "matched_skills":
                    sorted(matched_skills),

                "missing_skills":
                    sorted(missing_skills),

                "readiness_percentage":
                    round(readiness, 2)
            },

            status=status.HTTP_200_OK
        )

