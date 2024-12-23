# from rest_framework import serializers
from app.dynamic_serializer import DynamicFieldsModelSerializer
from app.models import Speciality


# class DoctorSerializer(serializers.ModelSerializer):
class SpecialitySerializer(DynamicFieldsModelSerializer):
  class Meta:
    model = Speciality
    fields = [
      'id',
      'title',
      'description'
    ]
