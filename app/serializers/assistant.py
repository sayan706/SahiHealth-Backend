from rest_framework import serializers
from app.models import Assistant
from app.serializers.profile import ProfileSerializer


class AssistantSerializer(serializers.ModelSerializer):
  profile = ProfileSerializer()

  class Meta:
    model = Assistant
    fields = ['id', 'profile', 'is_active', 'created_at', 'updated_at']
