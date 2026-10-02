from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password,check_password


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=6
    )

    class Meta:
        model = User
        fields = [
            'full_name',
            'email',
            'password',
            'education',
            'experience_years',
            'target_role'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = User.objects.create(
            **validated_data
        )

        user.password_hash = make_password(password)
        user.save()

        return user


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True
    )

    def validate(self, data):

        email = data['email']
        password = data['password']

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            raise serializers.ValidationError(
                "Invalid email or password."
            )

        if not user.password_hash:
            raise serializers.ValidationError(
                "Password is not set for this user."
            )

        if not check_password(
            password,
            user.password_hash
        ):
            raise serializers.ValidationError(
                "Invalid email or password."
            )

        data['user'] = user

        return data
    