from rest_framework import serializers
from app.dynamic_serializer import DynamicFieldsModelSerializer
from app.models import DietAdvice


class DietAdviceSerializer(DynamicFieldsModelSerializer):
  class Meta:
    model = DietAdvice
    # fields = '__all__'
    exclude = [
      'prescription',
      'is_active',
      'created_at',
      'updated_at'
    ]


class UpdateDietAdviceSerializer(DynamicFieldsModelSerializer):
  # Allow id to be optional to update
  id = serializers.IntegerField(required=False, allow_null=True)

  class Meta:
    model = DietAdvice
    fields = [
      'id',
      'description'
    ]
