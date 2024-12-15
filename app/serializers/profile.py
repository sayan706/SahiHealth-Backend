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
      'dp_url',
      'profile_picture',
      'role',
      'user',
      'is_active',
      'created_at',
      'updated_at',
    ]


class FileUploadSerializer(serializers.Serializer):
  file = serializers.FileField(required=True)
  file_ext = serializers.CharField(max_length=20, required=True)
  file_name = serializers.CharField(max_length=255, required=True)

  def validate_file_ext(self, value):
    allowed_extensions = ['jpg', 'png', 'jpeg', 'webp']

    if value.lower() not in allowed_extensions:
      raise serializers.ValidationError(f"File extension '{value}' is not allowed")

    return value

  def validate_file_name(self, value):
    if '/' in value or '\\' in value:
      raise serializers.ValidationError("File name must not contain slashes")

    return value
