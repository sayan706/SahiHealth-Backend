# from rest_framework import serializers
from app.dynamic_serializer import DynamicFieldsModelSerializer
from app.models import MedicineDoseType


class MedicineDoseTypeSerializer(DynamicFieldsModelSerializer):
  class Meta:
    model = MedicineDoseType
    # fields = '__all__'
    exclude = [
      'is_active',
      'created_at',
      'updated_at'
    ]
