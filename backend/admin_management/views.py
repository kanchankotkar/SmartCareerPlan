from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.authentication import CustomJWTAuthentication
from accounts.models import User

from careers.models import JobRole, JobRoleSkill
from skills.models import Skill
from skills.serializers import SkillSerializer

from learning.models import LearningResource, LearningProgress

from .serializers import (
    AdminUserSerializer,
    AdminJobRoleSerializer,
    AdminJobRoleSkillSerializer,
    AdminJobRoleWithSkillsSerializer,
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

class AdminUserUpdateView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAdminUser]

    def patch(self, request, user_id):

        user = User.objects.filter(user_id=user_id).first()

        if not user:
            return Response(
                {"error": "User not found"},
                status=404
            )

        serializer = AdminUserSerializer(
            user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            updated_user = serializer.save()

            return Response({
                "message": "User updated successfully",
                "user": AdminUserSerializer(updated_user).data
            }, status=200)

        return Response(
            serializer.errors,
            status=400
        )

class AdminUserDeleteView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAdminUser]

    def delete(self, request, user_id):

        user = User.objects.filter(user_id=user_id).first()

        if not user:
            return Response(
                {"error": "User not found"},
                status=404
            )

        # Check user skills
        from skills.models import UserSkill

        user_skill_count = UserSkill.objects.filter(
            user=user
        ).count()

        if user_skill_count > 0:
            return Response({
                "error": "Cannot delete this user because the user has skills.",
                "user_skills": user_skill_count
            }, status=409)

        # Check learning progress
        progress_count = LearningProgress.objects.filter(
            user=user
        ).count()

        if progress_count > 0:
            return Response({
                "error": "Cannot delete this user because learning progress exists.",
                "learning_progress": progress_count
            }, status=409)

        deleted_user_id = user.user_id
        deleted_user_email = user.email

        user.delete()

        return Response({
            "message": "User deleted successfully",
            "user_id": deleted_user_id,
            "email": deleted_user_email
        }, status=200)

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

class AdminJobRoleUpdateView(APIView):

    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAdminUser]

    def put(self, request, role_id):

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

        serializer = AdminJobRoleSerializer(
            role,
            data=request.data
        )

        if serializer.is_valid():

            updated_role = serializer.save()

            return Response(
                {
                    "message": "Job role updated successfully",
                    "role": AdminJobRoleSerializer(
                        updated_role
                    ).data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, role_id):

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

        serializer = AdminJobRoleSerializer(
            role,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            updated_role = serializer.save()

            return Response(
                {
                    "message": "Job role updated successfully",
                    "role": AdminJobRoleSerializer(
                        updated_role
                    ).data
                },
                status=status.HTTP_200_OK
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
    def get(self, request):

        resources = LearningResource.objects.all().select_related('skill')

        serializer = AdminLearningResourceSerializer(
            resources,
            many=True
        )

        return Response(
            {
                "total_resources": resources.count(),
                "resources": serializer.data
            },
            status=status.HTTP_200_OK
        ) 

class AdminLearningResourceBySkillView(APIView):

    authentication_classes = [
        CustomJWTAuthentication
    ]

    permission_classes = [
        IsAdminUser
    ]

    def get(self, request, skill_id):

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

        resources = LearningResource.objects.filter(
            skill=skill
        ).select_related('skill')

        serializer = AdminLearningResourceSerializer(
            resources,
            many=True
        )

        return Response(
            {
                "skill_id": skill.skill_id,
                "skill_name": skill.skill_name,
                "total_resources": resources.count(),
                "resources": serializer.data
            },
            status=status.HTTP_200_OK
        )


class AdminLearningResourceUpdateView(APIView):

    authentication_classes = [
        CustomJWTAuthentication
    ]

    permission_classes = [
        IsAdminUser
    ]

    def put(self, request, resource_id):

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

        serializer = AdminLearningResourceSerializer(
            resource,
            data=request.data
        )

        if serializer.is_valid():

            updated_resource = serializer.save()

            return Response(
                {
                    "message": "Learning resource updated successfully",
                    "resource": AdminLearningResourceSerializer(
                        updated_resource
                    ).data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, resource_id):

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

        serializer = AdminLearningResourceSerializer(
            resource,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            updated_resource = serializer.save()

            return Response(
                {
                    "message": "Learning resource updated successfully",
                    "resource": AdminLearningResourceSerializer(
                        updated_resource
                    ).data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    def delete(self, request, resource_id):

        resource = LearningResource.objects.filter(
            resource_id=resource_id
        ).first()

        # Check whether resource exists
        if not resource:
            return Response(
                {
                    "error": "Learning resource not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Check whether users have progress for this resource
        progress_count = LearningProgress.objects.filter(
            resource=resource
        ).count()

        if progress_count > 0:
            return Response(
                {
                    "error": "Cannot delete this learning resource because user progress records exist.",
                    "progress_records": progress_count
                },
                status=status.HTTP_409_CONFLICT
            )

        # Delete resource
        resource.delete()

        return Response(
            {
                "message": "Learning resource deleted successfully"
            },
            status=status.HTTP_200_OK
        )
class AdminJobRoleListView(APIView):

    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):

        roles = JobRole.objects.all()

        serializer = AdminJobRoleWithSkillsSerializer(
            roles,
            many=True
        )

        return Response(
            {
                "total_roles": roles.count(),
                "roles": serializer.data
            },
            status=status.HTTP_200_OK
        )

class AdminJobRoleDeleteView(APIView):

    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAdminUser]

    def delete(self, request, role_id):

        # 1. Find the job role
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

        # 2. Check whether users are assigned to this role
        user_count = User.objects.filter(
            target_role=role
        ).count()

        if user_count > 0:
            return Response(
                {
                    "error": "Cannot delete this job role because users are assigned to it.",
                    "assigned_users": user_count
                },
                status=status.HTTP_409_CONFLICT
            )

        # 3. Check whether skills are assigned to this role
        skill_count = JobRoleSkill.objects.filter(
            role=role
        ).count()

        if skill_count > 0:
            return Response(
                {
                    "error": "Cannot delete this job role because skills are assigned to it.",
                    "assigned_skills": skill_count
                },
                status=status.HTTP_409_CONFLICT
            )

        # 4. Delete the role
        role.delete()

        return Response(
            {
                "message": "Job role deleted successfully",
                "role_id": role_id
            },
            status=status.HTTP_200_OK
        )        
class AdminJobRoleSkillsListView(APIView):

    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, role_id):

        # 1. Check whether job role exists
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

        # 2. Get skills assigned to this role
        role_skills = JobRoleSkill.objects.filter(
            role=role
        ).select_related('skill')

        # 3. Serialize the data
        serializer = AdminJobRoleSkillSerializer(
            role_skills,
            many=True
        )

        return Response(
            {
                "role_id": role.role_id,
                "role_name": role.role_name,
                "total_skills": role_skills.count(),
                "skills": serializer.data
            },
            status=status.HTTP_200_OK
        )

class AdminJobRoleSkillUpdateView(APIView):

    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAdminUser]

    def patch(self, request, role_skill_id):

        # 1. Find the role-skill assignment
        role_skill = JobRoleSkill.objects.filter(
            role_skill_id=role_skill_id
        ).first()

        if not role_skill:
            return Response(
                {
                    "error": "Job role skill not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # 2. Update the data
        serializer = AdminJobRoleSkillSerializer(
            role_skill,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            updated_role_skill = serializer.save()

            return Response(
                {
                    "message": "Job role skill updated successfully",
                    "role_skill": AdminJobRoleSkillSerializer(
                        updated_role_skill
                    ).data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class AdminJobRoleSkillDeleteView(APIView):

    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAdminUser]

    def delete(self, request, role_skill_id):

        # 1. Find the role-skill assignment
        role_skill = JobRoleSkill.objects.filter(
            role_skill_id=role_skill_id
        ).first()

        if not role_skill:
            return Response(
                {
                    "error": "Job role skill not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # 2. Store IDs before deleting
        deleted_role_skill_id = role_skill.role_skill_id
        role_id = role_skill.role_id
        skill_id = role_skill.skill_id

        # 3. Delete assignment
        role_skill.delete()

        return Response(
            {
                "message": "Job role skill deleted successfully",
                "role_skill_id": deleted_role_skill_id,
                "role_id": role_id,
                "skill_id": skill_id
            },
            status=status.HTTP_200_OK
        )


class AdminSkillListView(APIView):

    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):

        skills = Skill.objects.all().order_by('skill_id')

        skill_data = []

        for skill in skills:
            skill_data.append({
                "skill_id": skill.skill_id,
                "skill_name": skill.skill_name,
                "category": skill.category,
                "description": skill.description,
                "created_at": skill.created_at
            })

        return Response(
            {
                "total_skills": skills.count(),
                "skills": skill_data
            },
            status=status.HTTP_200_OK
        )

class AdminSkillCreateView(APIView):

    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):

        serializer = SkillSerializer(
            data=request.data
        )

        if serializer.is_valid():

            skill = serializer.save()

            return Response(
                {
                    "message": "Skill created successfully",
                    "skill": SkillSerializer(skill).data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class AdminSkillUpdateView(APIView):

    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAdminUser]

    def patch(self, request, skill_id):

        # 1. Find skill
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

        # 2. Update skill
        serializer = SkillSerializer(
            skill,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            updated_skill = serializer.save()

            return Response(
                {
                    "message": "Skill updated successfully",
                    "skill": SkillSerializer(
                        updated_skill
                    ).data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )       

class AdminSkillDeleteView(APIView):

    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAdminUser]

    def delete(self, request, skill_id):

        # 1. Find skill
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

        # 2. Check job role assignments
        role_skill_count = JobRoleSkill.objects.filter(
            skill=skill
        ).count()

        if role_skill_count > 0:
            return Response(
                {
                    "error": "Cannot delete this skill because it is assigned to job roles.",
                    "assigned_job_roles": role_skill_count
                },
                status=status.HTTP_409_CONFLICT
            )

        # 3. Check user skill assignments
        from skills.models import UserSkill

        user_skill_count = UserSkill.objects.filter(
            skill=skill
        ).count()

        if user_skill_count > 0:
            return Response(
                {
                    "error": "Cannot delete this skill because users have this skill.",
                    "users_with_skill": user_skill_count
                },
                status=status.HTTP_409_CONFLICT
            )

        # 4. Check learning resources
        resource_count = LearningResource.objects.filter(
            skill=skill
        ).count()

        if resource_count > 0:
            return Response(
                {
                    "error": "Cannot delete this skill because learning resources are linked to it.",
                    "learning_resources": resource_count
                },
                status=status.HTTP_409_CONFLICT
            )

        # 5. Delete skill
        deleted_skill_id = skill.skill_id
        deleted_skill_name = skill.skill_name

        skill.delete()

        return Response(
            {
                "message": "Skill deleted successfully",
                "skill_id": deleted_skill_id,
                "skill_name": deleted_skill_name
            },
            status=status.HTTP_200_OK
        )

class AdminDashboardStatsView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):

        total_users = User.objects.count()
        total_skills = Skill.objects.count()
        total_job_roles = JobRole.objects.count()
        total_learning_resources = LearningResource.objects.count()
        total_progress_records = LearningProgress.objects.count()

        # Users by target role
        users_by_role = []

        for role in JobRole.objects.all().order_by('role_id'):
            user_count = User.objects.filter(
                target_role=role
            ).count()

            users_by_role.append({
                "role_id": role.role_id,
                "role_name": role.role_name,
                "user_count": user_count
            })

        # Skills by category
        skills_by_category = []

        categories = (
            Skill.objects
            .values('category')
            .distinct()
            .order_by('category')
        )

        for item in categories:
            category = item['category']

            skill_count = Skill.objects.filter(
                category=category
            ).count()

            skills_by_category.append({
                "category": category,
                "skill_count": skill_count
            })

            # Learning resources by skill
        resources_by_skill = []

        for skill in Skill.objects.all().order_by('skill_id'):
            resource_count = LearningResource.objects.filter(
                skill=skill
            ).count()

            if resource_count > 0:
                resources_by_skill.append({
                    "skill_id": skill.skill_id,
                    "skill_name": skill.skill_name,
                    "resource_count": resource_count
                })

        return Response({
        "total_users": total_users,
        "total_skills": total_skills,
        "total_job_roles": total_job_roles,
        "total_learning_resources": total_learning_resources,
        "total_progress_records": total_progress_records,
        "users_by_role": users_by_role,
        "skills_by_category": skills_by_category,
        "resources_by_skill": resources_by_skill
    }, status=200)