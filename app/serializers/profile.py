from rest_framework import serializers
from app.dynamic_serializer import DynamicFieldsModelSerializer
from app.models import Profile
from app.serializers.user import UserSerializer


# class ProfileSerializer(serializers.ModelSerializer):
class ProfileSerializer(DynamicFieldsModelSerializer):
  # user = UserSerializer()
  user = serializers.SerializerMethodField()

  def __init__(self, *args, **kwargs):
    # Extract nested serializer arguments
    user_fields = kwargs.pop('user_fields', None)
    user_exclude = kwargs.pop('user_exclude', None)

    # Initialize the parent class
    super().__init__(*args, **kwargs)

    # Store nested serializer arguments for later use
    self.user_fields = user_fields
    self.user_exclude = user_exclude

  def get_user(self, obj):
    # Pass the dynamic fields/exclude arguments to the nested ProfileSerializer
    return UserSerializer(
      obj.user,
      context=self.context,
      fields=self.user_fields,
      exclude=self.user_exclude
    ).data

  class Meta:
    model = Profile
    fields = '__all__'


class UpdateProfileSerializer(DynamicFieldsModelSerializer):
  class Meta:
    model = Profile
    fields = '__all__'
    read_only_fields = [
      'id',
      'user',
      'dp_url',
      'profile_picture',
      'created_at'
    ]


class FileUploadSerializer(serializers.Serializer):
  file = serializers.CharField(required=True)
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
