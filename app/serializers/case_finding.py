from rest_framework import serializers
from app.dynamic_serializer import DynamicFieldsModelSerializer
from app.models import CaseFinding


# class CaseFindingSerializer(serializers.ModelSerializer):
class CaseFindingSerializer(DynamicFieldsModelSerializer):
  class Meta:
    model = CaseFinding
    # fields = '__all__'
    exclude = [
      'case',
      'is_active',
      'created_at',
      'updated_at'
    ]


class CreateCaseFindingSerializer(DynamicFieldsModelSerializer):
  class Meta:
    model = CaseFinding
    fields = ['title']


class UpdateCaseFindingSerializer(DynamicFieldsModelSerializer):
  # Allow id to be optional to update
  id = serializers.IntegerField(required=False)

  class Meta:
    model = CaseFinding
    fields = [
      'id',
      'title'
    ]
