# from rest_framework import serializers
from app.dynamic_serializer import DynamicFieldsModelSerializer
from app.models import MedicineDoseRegimen


class MedicineDoseRegimenSerializer(DynamicFieldsModelSerializer):
  class Meta:
    model = MedicineDoseRegimen
    # fields = '__all__'
    exclude = [
      'is_active',
      'created_at',
      'updated_at'
    ]
