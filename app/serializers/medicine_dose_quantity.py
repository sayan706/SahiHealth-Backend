# from rest_framework import serializers
from app.dynamic_serializer import DynamicFieldsModelSerializer
from app.models import MedicineDoseQuantity


class MedicineDoseQuantitySerializer(DynamicFieldsModelSerializer):
  class Meta:
    model = MedicineDoseQuantity
    # fields = '__all__'
    exclude = [
      'is_active',
      'created_at',
      'updated_at'
    ]
