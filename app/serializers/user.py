from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
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
      'user_permissions',
    ]
