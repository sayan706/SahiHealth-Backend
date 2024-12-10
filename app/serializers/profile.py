from rest_framework import serializers
from app.models import Profile
from app.serializers.user import UserSerializer


class ProfileSerializer(serializers.ModelSerializer):
  user = UserSerializer()

  class Meta:
    model = Profile
    fields = [
      'id',
      'first_name',
      'last_name',
      'email',
      'phone_number',
      'gender',
      'location',
      'profile_picture',
      'role',
      'user',
      'is_active',
      'created_at',
      'updated_at',
    ]
