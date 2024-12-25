# from rest_framework import serializers
from app.dynamic_serializer import DynamicFieldsModelSerializer
from app.models import Case
from app.serializers.doctor import DoctorSerializer
from app.serializers.patient import PatientSerializer
from app.serializers.case_finding import CaseFindingSerializer
from app.serializers.case_document import CaseDocumentSerializer
from app.serializers.case_chief_complaint import CaseChiefComplaintSerializer


# class CaseSerializer(serializers.ModelSerializer):
class CaseSerializer(DynamicFieldsModelSerializer):
  patient = PatientSerializer(
    exclude=[
      'id',
      'created_by',
      'doctors',
      'phone_number',
      'address',
      'is_active',
      'created_at',
      'updated_at'
    ]
  )

  assigned_doctor = DoctorSerializer(
    fields=[
      'degree',
      'speciality',
      'profile'
    ],
    profile_fields=[
      'first_name',
      'last_name'
    ]
  )

  chief_complaints = CaseChiefComplaintSerializer(many=True)
  documents = CaseDocumentSerializer(many=True)
  findings = CaseFindingSerializer(many=True)

  class Meta:
    model = Case
    fields = [
      'id',
      'patient',
      'assigned_doctor',
      'chief_complaints',
      'findings',
      'past_treatment',
      'treatment_location',
      'treatment_type',
      'documents',
      'note',
      'follow_up_id',
      'follow_up_date',
      'is_active',
      'created_at',
      'updated_at'
    ]


class AppointmentSerializer(DynamicFieldsModelSerializer):
  patient = PatientSerializer(
    fields=[
      'full_name',
      'gender',
      'age',
      'phone_number'
    ]
  )

  assigned_doctor = DoctorSerializer(
    fields=[
      'degree',
      'profile'
    ],
    profile_fields=[
      'first_name',
      'last_name'
    ]
  )

  class Meta:
    model = Case
    fields = '__all__'
