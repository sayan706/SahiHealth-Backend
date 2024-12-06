from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime


# Create your views here.

class RoleViewset(viewsets.ModelViewSet):
    queryset= Role.objects.all()
    serializer_class = RoleSerializer


class DoctorandCompounderViewset(viewsets.ModelViewSet):
    queryset= DoctorsandCompunders.objects.all()
    serializer_class = DoctorandCompounderSerializer

class Register(APIView):
    @transaction.atomic
    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)

            if serializer.is_valid():
                user = serializer.save()
                token = Token.objects.create(user=user)

                return Response({
                    "message": f"User {serializer.data['username']} is created",
                    "token": token.key
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "error": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)



class Login(APIView):

    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            # Check if the username exists
            if not User.objects.filter(username=username).exists():
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "No user found!",
                    "errors": {
                        "name": "UserNotFound",
                        "error": "The username does not exist."
                    },
                    "timestamp": int(datetime.now().timestamp())
                }, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(username=username)

            # Check if the password is correct
            if not user.check_password(password):
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Wrong password!",
                    "errors": {
                        "name": "InvalidCredentials",
                        "error": "The password provided is incorrect."
                    },
                    "timestamp": int(datetime.now().timestamp())
                }, status=status.HTTP_400_BAD_REQUEST)

            # Generate or retrieve the token
            token, created = Token.objects.get_or_create(user=user)

            # Serialize the user data
            serializer = UserSerializer(user)

            # Successful login response
            return Response({
                "status": status.HTTP_200_OK,
                "message": "Logged in successfully!",
                "data": {
                    "user": serializer.data,
                    "token": token.key
                },
                "timestamp": int(datetime.now().timestamp())
            }, status=status.HTTP_200_OK)

        except Exception as e:
            # Generic error response
            return Response({
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "An error occurred during login.",
                "errors": {
                    "name": "InternalServerError",
                    "error": str(e)
                },
                "timestamp": int(datetime.now().timestamp())
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class Logout(APIView):
    def post(self, request):
        try:
            token_key = request.headers.get('Authorization').split()[1]
            token = Token.objects.get(key=token_key)
            token.delete()
            
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
            
        except Token.DoesNotExist:
            return Response({"message": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)