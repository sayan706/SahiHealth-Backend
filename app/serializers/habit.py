from rest_framework import serializers
from app.models import Habit


class HabitSerializer(serializers.ModelSerializer):
  class Meta:
    model = Habit
    fields = '__all__'
