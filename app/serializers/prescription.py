# from utils import exceptions
from app.dynamic_serializer import DynamicFieldsModelSerializer
from app.models import Doctor, Prescription, Medicine, DiagnosisItem, InvestigationItem, DietAdvice
from app.serializers.medicine import MedicineSerializer, CreateMedicineSerializer, UpdateMedicineSerializer
from app.serializers.diet_advice import DietAdviceSerializer, UpdateDietAdviceSerializer
from app.serializers.doctor import DoctorSerializer
from app.serializers.diagnosis_item import (
  DiagnosisItemSerializer,
  CreateDiagnosisItemSerializer,
  UpdateDiagnosisItemSerializer
)
from app.serializers.investigation_item import (
  InvestigationItemSerializer,
  CreateInvestigationItemSerializer,
  UpdateInvestigationItemSerializer
)


class PrescriptionSerializer(DynamicFieldsModelSerializer):
  medicines = MedicineSerializer(many=True)
  diagnosis_items = DiagnosisItemSerializer(many=True)
  investigation_items = InvestigationItemSerializer(many=True)
  diet_advices = DietAdviceSerializer(many=True)

  referred_doctors = DoctorSerializer(
    many=True,
    fields=[
      'profile',
      'speciality'
    ],
    profile_fields=['full_name']
  )

  class Meta:
    model = Prescription
    fields = [
      'id',
      'medicines',
      'diagnosis_items',
      'investigation_items',
      'diet_advices',
      'note',
      'referred_doctors',
      'created_at',
      'updated_at'
    ]


class CreatePrescriptionSerializer(DynamicFieldsModelSerializer):
  medicines = CreateMedicineSerializer(many=True)
  diagnosis_items = CreateDiagnosisItemSerializer(many=True)
  investigation_items = CreateInvestigationItemSerializer(many=True)
  diet_advices = DietAdviceSerializer(many=True)

  class Meta:
    model = Prescription
    fields = [
      'case',
      'medicines',
      'diagnosis_items',
      'investigation_items',
      'diet_advices',
      'note',
      'referred_doctors'
    ]

  # def validate(self, attrs):
  #   doctors = []
  #   referred_doctors = attrs.pop('referred_doctors', [])

  #   for referred_doctor in referred_doctors:
  #     try:
  #       doctor = Doctor.objects.get(id=referred_doctor)
  #       doctors.append(doctor)
  #     except Doctor.DoesNotExist:
  #       raise exceptions.DoesNotExistException(
  #         detail=f'No doctor found with id {referred_doctor}',
  #         code='Doctor not found'
  #       )

  #   # Attach validated instances to attrs for later use in create() or update()
  #   if len(referred_doctors) != 0:
  #     attrs['referred_doctors'] = doctors

  #   return attrs

  def create(self, validated_data):
    medicines = validated_data.pop('medicines', [])
    diagnosis_items = validated_data.pop('diagnosis_items', [])
    investigation_items = validated_data.pop('investigation_items', [])
    diet_advices = validated_data.pop('diet_advices', [])
    referred_doctors = validated_data.pop('referred_doctors', [])

    # Create prescription instance
    prescription = Prescription.objects.create(**validated_data)

    # Add medicines, diagnosis_items, investigation_items, diet_advices and referred_doctors
    for medicine in medicines:
      dose_regimens = medicine.pop('dose_regimens', [])
      medicine_instance = Medicine.objects.create(prescription=prescription, **medicine)

      for dose_regimen in dose_regimens:
        medicine_instance.dose_regimens.add(dose_regimen)

    for diagnosis_item in diagnosis_items:
      DiagnosisItem.objects.create(prescription=prescription, **diagnosis_item)

    for investigation_item in investigation_items:
      InvestigationItem.objects.create(prescription=prescription, **investigation_item)

    for diet_advice in diet_advices:
      DietAdvice.objects.create(prescription=prescription, **diet_advice)

    for referred_doctor in referred_doctors:
      prescription.referred_doctors.add(referred_doctor)

    prescription.case.is_completed = True
    prescription.case.save(update_fields=['is_completed'])

    return prescription


class UpdatePrescriptionSerializer(DynamicFieldsModelSerializer):
  medicines = UpdateMedicineSerializer(many=True)
  diagnosis_items = UpdateDiagnosisItemSerializer(many=True)
  investigation_items = UpdateInvestigationItemSerializer(many=True)
  diet_advices = UpdateDietAdviceSerializer(many=True)

  class Meta:
    model = Prescription
    fields = [
      'medicines',
      'diagnosis_items',
      'investigation_items',
      'diet_advices',
      'note',
      'referred_doctors'
    ]

  def update(self, instance, validated_data):
    medicines = validated_data.pop('medicines', [])
    diagnosis_items = validated_data.pop('diagnosis_items', [])
    investigation_items = validated_data.pop('investigation_items', [])
    diet_advices = validated_data.pop('diet_advices', [])
    referred_doctors = validated_data.pop('referred_doctors', [])

    for attr, value in validated_data.items():
      setattr(instance, attr, value)

    instance.save()

    # Update or add medicines, diagnosis_items, investigation_items, diet_advices and referred_doctors
    for medicine in medicines:
      medicine_id = medicine.get('id', None)
      dose_regimens = medicine.pop('dose_regimens', [])

      if medicine_id is not None:
        medicine_instance = Medicine.objects.get(id=medicine_id)
        medicine_instance.dose_regimens.clear()

        for attr, value in medicine.items():
          setattr(medicine_instance, attr, value)

        for dose_regimen in dose_regimens:
          medicine_instance.dose_regimens.add(dose_regimen)

        medicine_instance.save()
      else:
        medicine_instance = Medicine.objects.create(prescription=instance, **medicine)

        for dose_regimen in dose_regimens:
          medicine_instance.dose_regimens.add(dose_regimen)

    for diagnosis_item in diagnosis_items:
      diagnosis_item_id = diagnosis_item.get('id', None)

      if diagnosis_item_id is not None:
        diagnosis_item_instance = DiagnosisItem.objects.get(id=diagnosis_item_id)

        for attr, value in diagnosis_item.items():
          setattr(diagnosis_item_instance, attr, value)

        diagnosis_item_instance.save()
      else:
        DiagnosisItem.objects.create(prescription=instance, **diagnosis_item)

    for investigation_item in investigation_items:
      investigation_item_id = investigation_item.get('id', None)

      if investigation_item_id is not None:
        investigation_item_instance = InvestigationItem.objects.get(id=investigation_item_id)

        for attr, value in investigation_item.items():
          setattr(investigation_item_instance, attr, value)

        investigation_item_instance.save()
      else:
        InvestigationItem.objects.create(prescription=instance, **investigation_item)

    for diet_advice in diet_advices:
      diet_advice_id = diet_advice.get('id', None)

      if diet_advice_id is not None:
        diet_advice_instance = DietAdvice.objects.get(id=diet_advice_id)

        for attr, value in diet_advice.items():
          setattr(diet_advice_instance, attr, value)

        diet_advice_instance.save()
      else:
        DietAdvice.objects.create(prescription=instance, **diet_advice)

    if len(referred_doctors) != 0:
      instance.referred_doctors.clear()

    for referred_doctor in referred_doctors:
      instance.referred_doctors.add(referred_doctor)

    return instance
