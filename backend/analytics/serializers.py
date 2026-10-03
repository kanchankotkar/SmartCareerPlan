from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.authentication import CustomJWTAuthentication
from careers.models import JobRole, JobRoleSkill
from skills.models import UserSkill
from learning.models import LearningResource, LearningProgress


class DashboardAnalyticsView(APIView):

    authentication_classes = [CustomJWTAuthentication]

    def get(self, request):

        user = request.user

        # --------------------------------
        # 1. Check user's target role
        # --------------------------------

        if not user.target_role:

            return Response(
                {
                    "error": "Target job role is not selected."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        role = user.target_role

        # --------------------------------
        # 2. Required skills
        # --------------------------------

        required_skills = JobRoleSkill.objects.filter(
            role=role
        ).select_related('skill')

        # --------------------------------
        # 3. User skills
        # --------------------------------

        user_skills = UserSkill.objects.filter(
            user=user
        ).select_related('skill')

        required_skill_names = {
            item.skill.skill_name
            for item in required_skills
        }

        user_skill_names = {
            item.skill.skill_name
            for item in user_skills
        }

        # --------------------------------
        # 4. Matched and missing skills
        # --------------------------------

        matched_skills = (
            required_skill_names
            .intersection(user_skill_names)
        )

        missing_skills = (
            required_skill_names
            - user_skill_names
        )

        # --------------------------------
        # 5. Readiness percentage
        # --------------------------------

        total_required = len(required_skill_names)

        if total_required > 0:

            readiness = (
                len(matched_skills)
                / total_required
            ) * 100

        else:

            readiness = 0

        # --------------------------------
        # 6. Learning resources
        # --------------------------------

        resources = LearningResource.objects.all()

        total_resources = resources.count()

        # --------------------------------
        # 7. User learning progress
        # --------------------------------

        progress_records = LearningProgress.objects.filter(
            user=user
        )

        started_resources = progress_records.filter(
            progress_percentage__gt=0
        ).count()

        completed_resources = progress_records.filter(
            progress_percentage=100
        ).count()

        # --------------------------------
        # 8. Average progress
        # --------------------------------

        total_progress = 0

        for progress in progress_records:

            total_progress += float(
                progress.progress_percentage or 0
            )

        progress_count = progress_records.count()

        if progress_count > 0:

            average_progress = (
                total_progress / progress_count
            )

        else:

            average_progress = 0

        # --------------------------------
        # 9. Dashboard response
        # --------------------------------

        return Response(
            {
                "user": {
                    "user_id": user.user_id,
                    "full_name": user.full_name,
                    "email": user.email,
                    "target_role": role.role_name
                },

                "readiness": {
                    "total_required_skills": total_required,
                    "matched_skills": len(matched_skills),
                    "missing_skills": len(missing_skills),
                    "readiness_percentage": round(
                        readiness,
                        2
                    )
                },

                "skills": {
                    "matched": sorted(
                        matched_skills
                    ),
                    "missing": sorted(
                        missing_skills
                    )
                },

                "learning": {
                    "total_resources": total_resources,
                    "started_resources": started_resources,
                    "completed_resources": completed_resources,
                    "average_progress": round(
                        average_progress,
                        2
                    )
                }
            },
            status=status.HTTP_200_OK
        )