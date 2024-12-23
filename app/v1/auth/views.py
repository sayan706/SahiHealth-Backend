from utils import exceptions
from app.serializers.doctor import DoctorSerializer
from app.serializers.assistant import AssistantSerializer
from django.shortcuts import render
from rest_framework.views import APIView
from utils.response_handler import custom_response_handler
from rest_framework import status
from app.models import Profile, Doctor, Assistant
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class LoginAPIView(APIView):
  authentication_classes = []
  permission_classes = []

  def post(self, request, format=None):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
      raise exceptions.InvalidRequestBodyException(
        detail={
          'error': ['Both username and password is required']
        },
        code="Missing Credentials"
      )

    # Check if the username exists
    if not User.objects.filter(username=username).exists():
      raise exceptions.DoesNotExistException(
        detail=f"Username '{username}' does not exist",
        code="Username Not Found"
      )

    user = User.objects.get(username=username)

    # Check if the password is correct
    if not user.check_password(password):
      raise exceptions.GenericException(
        detail=f"Wrong password for username '{username}'",
        code="Incorrect Password"
      )

    # Generate or retrieve the token
    token, created = Token.objects.get_or_create(user=user)

    # Serialize the user data
    serializedUserData = None
    profile = Profile.objects.get(user=user)

    if profile.role == 'DOCTOR':
      doctor = Doctor.objects.get(profile=profile)
      serializedUserData = DoctorSerializer(
        instance=doctor,
        exclude=[
          'degree',
          'speciality',
          'is_active',
          'created_at',
          'updated_at'
        ],
        profile_fields=[
          'first_name',
          'last_name',
          'dp_url',
          'role'
        ],
        profile_exclude=[
          'id',
          'user',
          'is_active',
          'created_at',
          'updated_at'
        ]
      )
    elif profile.role == 'ASSISTANT':
      assistant = Assistant.objects.get(profile=profile)
      serializedUserData = AssistantSerializer(
        instance=assistant,
        profile_exclude=[
          'id',
          'is_active',
          'created_at',
          'updated_at'
        ],
        user_fields=[
          'username',
          'last_login',
          'date_joined',
          'user_permissions'
        ]
      )
    else:
      raise exceptions.GenericException(
        detail=f"Either 'DOCTOR' or 'ASSISTANT' is allowed as a role",
        code="Invalid User Role"
      )

    return custom_response_handler(
      status=status.HTTP_200_OK,
      message="Login Successful",
      data={
        'token': token.key,
        'user_data': serializedUserData.data
      }
    )


class LogoutAPIView(APIView):
  def delete(self, request, format=None):
    token_key = request.headers.get('Authorization').split()[1]
    token = Token.objects.get(key=token_key)
    token.delete()

    return custom_response_handler(
      status=status.HTTP_200_OK,
      message="Logout Successful",
      data="You have successfully logged out"
    )
