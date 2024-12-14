from rest_framework import serializers
from app.models import Patient

class PatientSerializer(serializers.ModelSerializer):
  class Meta:
    model = Patient
    fields = ['id', 'name', 'age', 'email', 'phone_number', 'gender', 'address', 'created_by', 'created_at', 'updated_at']