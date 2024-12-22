# from rest_framework import serializers
from app.dynamic_serializer import DynamicFieldsModelSerializer
from app.models import CaseDocument


# class CaseDocumentSerializer(serializers.ModelSerializer):
class CaseDocumentSerializer(DynamicFieldsModelSerializer):
  class Meta:
    model = CaseDocument
    # fields = '__all__'
    exclude = ['case', 'is_active', 'created_at', 'updated_at']
