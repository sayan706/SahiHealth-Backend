from utils import exceptions
from rest_framework import serializers
from app.dynamic_serializer import DynamicFieldsModelSerializer
from app.models import Doctor, Patient, Case, CaseChiefComplaint, CaseDocument, CaseFinding
from app.serializers.doctor import DoctorSerializer
from app.serializers.patient import PatientSerializer
from app.serializers.case_document import CaseDocumentSerializer
from app.serializers.case_finding import CaseFindingSerializer, UpdateCaseFindingSerializer
from app.serializers.case_chief_complaint import (
  CaseChiefComplaintSerializer, UpdateCaseChiefComplaintSerializer
)


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
      'blood_pressure_low',
      'blood_pressure_high',
      'blood_sugar_level',
      'pulse',
      'oxygen',
      'body_temperature',
      'weight',
      'note_on_vitals',
      'complaint_severity',
      'past_treatment',
      'treatment_location',
      'treatment_type',
      'documents',
      'note',
      'follow_up_id',
      'follow_up_date',
      'is_completed',
      'is_active',
      'created_at',
      'updated_at'
    ]


class CreateCaseSerializer(DynamicFieldsModelSerializer):
  doctor_id = serializers.IntegerField(write_only=True)
  patient_id = serializers.IntegerField(write_only=True)

  # chief_complaints = serializers.ListField(write_only=True)
  # documents = serializers.ListField(write_only=True)
  # findings = serializers.ListField(write_only=True)

  class Meta:
    model = Case
    fields = [
      'patient_id',
      'doctor_id',
      # 'chief_complaints',
      'blood_pressure_low',
      'blood_pressure_high',
      'blood_sugar_level',
      'pulse',
      'oxygen',
      'body_temperature',
      'weight',
      'note_on_vitals',
      'complaint_severity',
      'past_treatment',
      'treatment_location',
      'treatment_type',
      # 'documents',
      # 'findings',
      'note',
      'follow_up_id',
      'follow_up_date'
    ]

  def validate(self, attrs):
    doctor = None
    patient = None
    doctor_id = attrs.get('doctor_id', None)
    patient_id = attrs.get('patient_id', None)

    if doctor_id is not None:
      try:
        doctor = Doctor.objects.get(id=doctor_id)
      except Doctor.DoesNotExist:
        raise exceptions.DoesNotExistException(
          detail=f'No doctor found with id {doctor_id}',
          code='Doctor not found'
        )

    if patient_id is not None:
      try:
        patient = Patient.objects.get(id=patient_id)
      except Patient.DoesNotExist:
        raise exceptions.DoesNotExistException(
          detail=f'No patient found with id {patient_id}',
          code='Patient not found'
        )

    # Attach validated instances to attrs for later use in create() or update()
    if doctor is not None:
      attrs['assigned_doctor'] = doctor
    if patient is not None:
      attrs['patient'] = patient

    # Remove after usecase as these fields are not in Patient
    if doctor_id is not None:
      attrs.pop('doctor_id')
    if patient_id is not None:
      attrs.pop('patient_id')

    return attrs

  def create(self, validated_data):
    # chief_complaints = validated_data.pop('chief_complaints', [])
    # documents = validated_data.pop('documents', [])
    # findings = validated_data.pop('findings', [])

    # Create case instance
    case = Case.objects.create(**validated_data)

    # # Create chief complaints, documents and findings
    # for chief_complaint in chief_complaints:
    #   CaseChiefComplaint.objects.create(
    #     case=case,
    #     title=chief_complaint.get('title', None),
    #     severity=chief_complaint.get('severity', None),
    #     duration=chief_complaint.get('duration', None),
    #     duration_unit=chief_complaint.get('duration_unit', None)
    #   )

    # for document in documents:
    #   CaseDocument.objects.create(
    #     case=case,
    #     file_name=document.get('file_name', None),
    #     file_extension=document.get('file_extension', None),
    #     file_url=document.get('file_url', None),
    #     document_section=document.get('document_section', None)
    #   )

    # for finding in findings:
    #   CaseFinding.objects.create(case=case, title=finding)

    case.patient.doctors.add(case.assigned_doctor)

    return case


class UpdateCaseSerializer(DynamicFieldsModelSerializer):
  chief_complaints = UpdateCaseChiefComplaintSerializer(many=True)
  findings = UpdateCaseFindingSerializer(many=True)

  class Meta:
    model = Case
    fields = [
      'chief_complaints',
      'blood_pressure_low',
      'blood_pressure_high',
      'blood_sugar_level',
      'pulse',
      'oxygen',
      'body_temperature',
      'weight',
      'note_on_vitals',
      'complaint_severity',
      'past_treatment',
      'treatment_location',
      'treatment_type',
      'findings',
      'note'
    ]

  def update(self, instance, validated_data):
    chief_complaints = validated_data.pop('chief_complaints', [])
    findings = validated_data.pop('findings', [])

    for attr, value in validated_data.items():
      setattr(instance, attr, value)

    instance.save()

    # instance.chief_complaints.clear()
    # for chief_complaint in chief_complaints:
    #   CaseChiefComplaint.objects.create(case=instance, **chief_complaint)

    # instance.findings.clear()
    # for finding in findings:
    #   CaseFinding.objects.create(case=instance, **finding)

    for chief_complaint in chief_complaints:
      chief_complaint_id = chief_complaint.get('id', None)

      if chief_complaint_id is not None:
        chief_complaint_instance = CaseChiefComplaint.objects.get(id=chief_complaint_id)

        for attr, value in chief_complaint.items():
          setattr(chief_complaint_instance, attr, value)

        chief_complaint_instance.save()
      else:
        CaseChiefComplaint.objects.create(case=instance, **chief_complaint)

    for finding in findings:
      finding_id = finding.get('id', None)

      if finding_id is not None:
        finding_instance = CaseFinding.objects.get(id=finding_id)

        for attr, value in finding.items():
          setattr(finding_instance, attr, value)

        finding_instance.save()
      else:
        CaseFinding.objects.create(case=instance, **finding)

    return instance
