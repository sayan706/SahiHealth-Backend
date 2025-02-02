from rest_framework import serializers
from app.dynamic_serializer import DynamicFieldsModelSerializer
from app.models import Medicine


class MedicineSerializer(DynamicFieldsModelSerializer):
  name = serializers.SlugRelatedField(read_only=True, slug_field='name')
  dose_type = serializers.SlugRelatedField(read_only=True, slug_field='name')
  dose_quantity = serializers.SlugRelatedField(read_only=True, slug_field='quantity')
  dose_regimens = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
  dose_duration = serializers.SlugRelatedField(read_only=True, slug_field='duration')

  class Meta:
    model = Medicine
    # fields = '__all__'
    exclude = [
      'prescription',
      'is_active',
      'created_at',
      'updated_at'
    ]


class CreateMedicineSerializer(DynamicFieldsModelSerializer):
  class Meta:
    model = Medicine
    # fields = '__all__'
    exclude = [
      'prescription',
      'is_active',
      'created_at',
      'updated_at'
    ]
