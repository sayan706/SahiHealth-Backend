from rest_framework import serializers
from app.dynamic_serializer import DynamicFieldsModelSerializer
from app.models import CaseDocument


# class CaseDocumentSerializer(serializers.ModelSerializer):
class CaseDocumentSerializer(DynamicFieldsModelSerializer):
  class Meta:
    model = CaseDocument
    # fields = '__all__'
    exclude = [
      'case',
      'is_active',
      'created_at',
      'updated_at'
    ]


class UpdateCaseDocumentSerializer(DynamicFieldsModelSerializer):
  # Either remove extra_kwargs or enable the following CharField
  # file_name = serializers.CharField(write_only=True)

  class Meta:
    model = CaseDocument
    fields = ['file_name']
    extra_kwargs = {
      'file_name': {'write_only': True}
    }


class DocumentsUploadSerializer(serializers.Serializer):
  DOCUMENT_SECTION_CHOICES = [
    "MEDICINE_PHOTO",
    "LAB_REPORT",
    "PHOTO"
  ]

  case_id = serializers.IntegerField()
  document_section = serializers.ChoiceField(choices=DOCUMENT_SECTION_CHOICES)
  files = serializers.ListField(child=serializers.FileField(), allow_empty=False)
