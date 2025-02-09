# from rest_framework import serializers
from app.dynamic_serializer import DynamicFieldsModelSerializer
from app.models import Investigation


class InvestigationSerializer(DynamicFieldsModelSerializer):
  class Meta:
    model = Investigation
    # fields = '__all__'
    exclude = [
      'is_active',
      'created_at',
      'updated_at'
    ]
