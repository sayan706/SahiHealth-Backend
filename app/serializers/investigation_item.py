from rest_framework import serializers
from app.dynamic_serializer import DynamicFieldsModelSerializer
from app.models import InvestigationItem


class InvestigationItemSerializer(DynamicFieldsModelSerializer):
  investigation = serializers.SlugRelatedField(read_only=True, slug_field='title')

  class Meta:
    model = InvestigationItem
    # fields = '__all__'
    exclude = [
      'prescription',
      'is_active',
      'created_at',
      'updated_at'
    ]


class CreateInvestigationItemSerializer(DynamicFieldsModelSerializer):
  class Meta:
    model = InvestigationItem
    # fields = '__all__'
    exclude = [
      'prescription',
      'is_active',
      'created_at',
      'updated_at'
    ]


class UpdateInvestigationItemSerializer(DynamicFieldsModelSerializer):
  # Allow id to be optional to update
  id = serializers.IntegerField(required=False, allow_null=True)

  class Meta:
    model = InvestigationItem
    fields = [
      'id',
      'investigation'
    ]
