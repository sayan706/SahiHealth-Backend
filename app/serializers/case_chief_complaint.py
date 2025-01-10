# from rest_framework import serializers
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
