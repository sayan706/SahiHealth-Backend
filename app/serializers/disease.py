# from rest_framework import serializers
from app.dynamic_serializer import DynamicFieldsModelSerializer
from app.models import Disease


# class DiseaseSerializer(serializers.ModelSerializer):
class DiseaseSerializer(DynamicFieldsModelSerializer):
  class Meta:
    model = Disease
    fields = '__all__'
