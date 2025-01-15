from rest_framework import serializers
from app.dynamic_serializer import DynamicFieldsModelSerializer
from app.models import CaseChiefComplaint


# class CaseChiefComplaintSerializer(serializers.ModelSerializer):
class CaseChiefComplaintSerializer(DynamicFieldsModelSerializer):
  class Meta:
    model = CaseChiefComplaint
    # fields = '__all__'
    exclude = [
      'case',
      'is_active',
      'created_at',
      'updated_at'
    ]


class CreateCaseChiefComplaintSerializer(DynamicFieldsModelSerializer):
  class Meta:
    model = CaseChiefComplaint
    fields = [
      'title',
      # 'severity',
      'duration',
      'duration_unit'
    ]


class UpdateCaseChiefComplaintSerializer(DynamicFieldsModelSerializer):
  # Allow id to be optional to update
  id = serializers.IntegerField(required=False)

  class Meta:
    model = CaseChiefComplaint
    fields = [
      'id',
      'title',
      # 'severity',
      'duration',
      'duration_unit'
    ]
