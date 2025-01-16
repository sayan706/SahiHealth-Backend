from rest_framework import serializers
from app.dynamic_serializer import DynamicFieldsModelSerializer
from app.models import CaseFinding
from app.serializers.finding_image import FindingImageSerializer


# class CaseFindingSerializer(serializers.ModelSerializer):
class CaseFindingSerializer(DynamicFieldsModelSerializer):
  finding_images = FindingImageSerializer(many=True)

  class Meta:
    model = CaseFinding
    fields = [
      'id',
      'title',
      'severity',
      'finding_images'
    ]
    # exclude = [
    #   'case',
    #   'is_active',
    #   'created_at',
    #   'updated_at'
    # ]


class CreateCaseFindingSerializer(DynamicFieldsModelSerializer):
  class Meta:
    model = CaseFinding
    fields = ['title']


class UpdateCaseFindingSerializer(DynamicFieldsModelSerializer):
  # Allow id to be optional to update
  id = serializers.IntegerField(required=False)
  images = serializers.ListField(write_only=True)

  class Meta:
    model = CaseFinding
    fields = [
      'id',
      'title',
      'severity',
      'images'
    ]
