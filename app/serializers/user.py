# from rest_framework import serializers
from app.dynamic_serializer import DynamicFieldsModelSerializer
from django.contrib.auth.models import User


# class UserSerializer(serializers.ModelSerializer):
class UserSerializer(DynamicFieldsModelSerializer):
  class Meta:
    model = User
    fields = [
      'id',
      'last_login',
      'is_superuser',
      'username',
      'is_staff',
      'is_active',
      'date_joined',
      'user_permissions'
    ]
