from utils import exceptions
from rest_framework import serializers
from app.dynamic_serializer import DynamicFieldsModelSerializer
from app.models import Profile, Doctor, Patient
from app.serializers.profile import ProfileSerializer
from app.serializers.disease import DiseaseSerializer
from app.serializers.habit import HabitSerializer


# class PatientSerializer(serializers.ModelSerializer):
class PatientSerializer(DynamicFieldsModelSerializer):
  created_by = ProfileSerializer(fields=[
    'id',
    'first_name',
    'last_name',
    'dp_url',
    'role',
  ])

  # diseases = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
  # habits = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')

  diseases = DiseaseSerializer(many=True, fields=[
    'id',
    'name'
  ])

  habits = HabitSerializer(many=True, fields=[
    'id',
    'name'
  ])

  class Meta:
    model = Patient
    fields = '__all__'


class CreatePatientSerializer(serializers.ModelSerializer):
  doctor_id = serializers.IntegerField(write_only=True)
  creator_profile_id = serializers.IntegerField(write_only=True)

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
      'other_diseases',
      'other_habits'
    ]

  def validate(self, attrs):
    try:
      doctor = Doctor.objects.get(id=attrs['doctor_id'])
    except Doctor.DoesNotExist:
      raise exceptions.DoesNotExistException(
        detail=f'No doctor found with id {attrs["doctor_id"]}',
        code='Doctor not found'
      )

    try:
      creator_profile = Profile.objects.get(id=attrs['creator_profile_id'])
    except Profile.DoesNotExist:
      raise exceptions.DoesNotExistException(
        detail=f'No profile found with id {attrs["creator_profile_id"]}',
        code='Profile not found'
      )

    # Attach validated instances to attrs to use in create()
    attrs['doctor'] = doctor
    attrs['creator_profile'] = creator_profile

    # Removing after usecase as these fields are not in Patient
    attrs.pop('doctor_id')
    attrs.pop('creator_profile_id')

    return attrs

  def create(self, validated_data):
    doctor = validated_data.pop('doctor')
    creator_profile = validated_data.pop('creator_profile')

    # Create patient instance
    patient = Patient.objects.create(created_by=creator_profile, **validated_data)

    # Associate the doctor with the patient
    patient.doctors.add(doctor)

    return patient
