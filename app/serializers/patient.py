from rest_framework import serializers
from app.models import Patient
from app.serializers.profile import ProfileSerializer
from app.serializers.doctor import DoctorSerializer


class PatientSerializer(serializers.ModelSerializer):
  created_by = ProfileSerializer()
  assigned_doctor = DoctorSerializer()

  class Meta:
    model = Patient
    fields = '__all__'
    # exclude = ['assigned_doctor']
    # fields = [
    #   'id',
    #   'full_name',
    #   'phone_number',
    #   'gender',
    #   'age',
    #   'address',
    #   'allergy',
    #   'blood_pressure',
    #   'pulse',
    #   'oxygen',
    #   'body_temp',
    #   'weight',
    #   'note_on_vitals',
    #   'diseases',
    #   'other_diseases',
    #   'habits',
    #   'other_habits',
    #   'is_active',
    #   'created_at',
    #   'updated_at'
    # ]
