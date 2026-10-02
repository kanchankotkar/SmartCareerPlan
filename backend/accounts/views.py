from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, LoginSerializer
from .models import User
from .authentication import CustomJWTAuthentication
class RegisterView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data
        )

        if serializer.is_valid():

            user = serializer.save()

            return Response(
                {
                    "message": "Registration successful",
                    "user_id": user.user_id,
                    "full_name": user.full_name,
                    "email": user.email
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class LoginView(APIView):

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        if serializer.is_valid():

            user = serializer.validated_data['user']

            refresh = RefreshToken()

            refresh['user_id'] = user.user_id
            refresh['email'] = user.email

            return Response(
                {
                    "message": "Login successful",
                    "user_id": user.user_id,
                    "full_name": user.full_name,
                    "email": user.email,
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
# profile view
class ProfileView(APIView):

    authentication_classes = [CustomJWTAuthentication]

    def get(self, request):

        user = request.user

        return Response(
            {
                "user_id": user.user_id,
                "full_name": user.full_name,
                "email": user.email,
                "education": user.education,
                "experience_years": user.experience_years,
                "target_role": user.target_role_id
            },
            status=status.HTTP_200_OK
        )