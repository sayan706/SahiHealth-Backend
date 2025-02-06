# from rest_framework import serializers
from app.dynamic_serializer import DynamicFieldsModelSerializer
from app.models import MedicineName


class MedicineNameSerializer(DynamicFieldsModelSerializer):
  class Meta:
    model = MedicineName
    # fields = '__all__'
    exclude = [
      'is_active',
      'created_at',
      'updated_at'
    ]
