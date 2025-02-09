# from rest_framework import serializers
from app.dynamic_serializer import DynamicFieldsModelSerializer
from app.models import Diagnosis


class DiagnosisSerializer(DynamicFieldsModelSerializer):
  class Meta:
    model = Diagnosis
    # fields = '__all__'
    exclude = [
      'is_active',
      'created_at',
      'updated_at'
    ]
