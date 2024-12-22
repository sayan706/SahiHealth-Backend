# from rest_framework import serializers
from app.dynamic_serializer import DynamicFieldsModelSerializer
from app.models import Habit


# class HabitSerializer(serializers.ModelSerializer):
class HabitSerializer(DynamicFieldsModelSerializer):
  class Meta:
    model = Habit
    fields = '__all__'
