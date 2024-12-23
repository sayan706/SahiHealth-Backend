from rest_framework import serializers
from app.dynamic_serializer import DynamicFieldsModelSerializer
from app.models import Doctor
from app.serializers.profile import ProfileSerializer
from app.serializers.speciality import SpecialitySerializer


# class DoctorSerializer(serializers.ModelSerializer):
class DoctorSerializer(DynamicFieldsModelSerializer):
  # profile = ProfileSerializer()
  profile = serializers.SerializerMethodField()
  speciality = SpecialitySerializer(exclude=['id'])

  def __init__(self, *args, **kwargs):
    # Extract nested serializer arguments
    user_fields = kwargs.pop('user_fields', None)
    user_exclude = kwargs.pop('user_exclude', None)
    profile_fields = kwargs.pop('profile_fields', None)
    profile_exclude = kwargs.pop('profile_exclude', None)

    # Initialize the parent class
    super().__init__(*args, **kwargs)

    # Store nested serializer arguments for later use
    self.user_fields = user_fields
    self.user_exclude = user_exclude
    self.profile_fields = profile_fields
    self.profile_exclude = profile_exclude

  def get_profile(self, obj):
    # Pass the dynamic fields/exclude arguments to the nested ProfileSerializer
    return ProfileSerializer(
      obj.profile,
      context=self.context,
      fields=self.profile_fields,
      exclude=self.profile_exclude,
      user_fields=self.user_fields,
      user_exclude=self.user_exclude,
    ).data

  class Meta:
    model = Doctor
    fields = [
      'id',
      'profile',
      'degree',
      'speciality',
      'is_active',
      'created_at',
      'updated_at'
    ]
