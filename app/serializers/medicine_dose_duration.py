# from rest_framework import serializers
from app.dynamic_serializer import DynamicFieldsModelSerializer
from app.models import MedicineDoseDuration


class MedicineDoseDurationSerializer(DynamicFieldsModelSerializer):
  class Meta:
    model = MedicineDoseDuration
    # fields = '__all__'
    exclude = [
      'is_active',
      'created_at',
      'updated_at'
    ]
