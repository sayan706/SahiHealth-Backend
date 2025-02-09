from rest_framework import serializers
from app.dynamic_serializer import DynamicFieldsModelSerializer
from app.models import DiagnosisItem


class DiagnosisItemSerializer(DynamicFieldsModelSerializer):
  diagnosis = serializers.SlugRelatedField(read_only=True, slug_field='title')

  class Meta:
    model = DiagnosisItem
    # fields = '__all__'
    exclude = [
      'prescription',
      'is_active',
      'created_at',
      'updated_at'
    ]


class CreateDiagnosisItemSerializer(DynamicFieldsModelSerializer):
  class Meta:
    model = DiagnosisItem
    # fields = '__all__'
    exclude = [
      'prescription',
      'is_active',
      'created_at',
      'updated_at'
    ]


class UpdateDiagnosisItemSerializer(DynamicFieldsModelSerializer):
  # Allow id to be optional to update
  id = serializers.IntegerField(required=False, allow_null=True)

  class Meta:
    model = DiagnosisItem
    fields = [
      'id',
      'diagnosis'
    ]
