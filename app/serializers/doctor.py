from rest_framework import serializers
from app.models import Doctor
from app.serializers.profile import ProfileSerializer


class DoctorSerializer(serializers.ModelSerializer):
  profile = ProfileSerializer()

  class Meta:
    model = Doctor
    fields = ['id', 'profile', 'speciality', 'is_active', 'created_at', 'updated_at']
