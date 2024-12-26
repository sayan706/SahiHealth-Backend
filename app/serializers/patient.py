from utils import exceptions
from rest_framework import serializers
from app.dynamic_serializer import DynamicFieldsModelSerializer
from app.models import Profile, Doctor, Patient
from app.serializers.profile import ProfileSerializer
from app.serializers.disease import DiseaseSerializer
from app.serializers.habit import HabitSerializer


# class PatientSerializer(serializers.ModelSerializer):
class PatientSerializer(DynamicFieldsModelSerializer):
  # diseases = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
  # habits = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')

  created_by = ProfileSerializer(
    fields=[
      'first_name',
      'last_name',
      'dp_url',
      'role'
    ]
  )

  diseases = DiseaseSerializer(
    many=True,
    fields=[
      'id',
      'name'
    ]
  )

  habits = HabitSerializer(
    many=True,
    fields=[
      'id',
      'name'
    ]
  )

  class Meta:
    model = Patient
    fields = '__all__'


class CreatePatientSerializer(serializers.ModelSerializer):
  doctor_id = serializers.IntegerField(write_only=True)
  creator_profile_id = serializers.IntegerField(write_only=True)

  diseases = serializers.ListField(write_only=True)
  habits = serializers.ListField(write_only=True)

  class Meta:
    model = Patient
    fields = [
      'doctor_id',
      'creator_profile_id',
      'full_name',
      'phone_number',
      'gender',
      'age',
      'address',
      'allergy',
      'blood_pressure',
      'pulse',
      'oxygen',
      'body_temperature',
      'weight',
      'note_on_vitals',
      'diseases',
      'other_diseases',
      'habits',
      'other_habits'
    ]

  def validate(self, attrs):
    doctor = None
    profile = None
    doctor_id = attrs.get('doctor_id', None)
    creator_profile_id = attrs.get('creator_profile_id', None)

    if doctor_id is not None:
      try:
        doctor = Doctor.objects.get(id=doctor_id)
      except Doctor.DoesNotExist:
        raise exceptions.DoesNotExistException(
          detail=f'No doctor found with id {doctor_id}',
          code='Doctor not found'
        )

    if creator_profile_id is not None:
      try:
        profile = Profile.objects.get(id=creator_profile_id)
      except Profile.DoesNotExist:
        raise exceptions.DoesNotExistException(
          detail=f'No profile found with id {creator_profile_id}',
          code='Profile not found'
        )

    # Attach validated instances to attrs for later use in create() or update()
    if doctor is not None:
      attrs['doctor'] = doctor
    if profile is not None:
      attrs['created_by'] = profile

    # Remove after usecase as these fields are not in Patient
    if doctor_id is not None:
      attrs.pop('doctor_id')
    if creator_profile_id is not None:
      attrs.pop('creator_profile_id')

    return attrs

  def create(self, validated_data):
    doctor = validated_data.pop('doctor')
    diseases = validated_data.pop('diseases')
    habits = validated_data.pop('habits')
    # created_by = validated_data.pop('created_by')

    # Create patient instance
    patient = Patient.objects.create(**validated_data)
    # patient = Patient.objects.create(created_by=created_by, **validated_data)

    # Associate the doctor with the patient
    patient.doctors.add(doctor)

    # Associate diseases with the patient
    for disease in diseases:
      patient.diseases.add(disease)

    # Associate habits with the patient
    for habit in habits:
      patient.habits.add(habit)

    return patient
