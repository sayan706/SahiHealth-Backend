from rest_framework import serializers
from app.dynamic_serializer import DynamicFieldsModelSerializer
from app.models import FindingImage


class FindingImageSerializer(DynamicFieldsModelSerializer):
  class Meta:
    model = FindingImage
    # fields = '__all__'
    exclude = [
      'case_finding',
      'is_active',
      'created_at',
      'updated_at'
    ]


class ImagesUploadSerializer(serializers.Serializer):
  case_id = serializers.IntegerField()
  files = serializers.ListField(child=serializers.FileField(), allow_empty=False)
