from django.contrib import admin
from .models import (
  Profile,
  Speciality,
  Doctor,
  Assistant,
  Disease,
  Habit,
  Patient,
  Case,
  CaseChiefComplaint,
  CaseFinding,
  FindingImage,
  CaseDocument,
  Prescription,
  MedicineDoseType,
  MedicineName,
  MedicineDoseQuantity,
  MedicineDoseRegimen,
  MedicineDoseDuration,
  Medicine,
  DietAdvice
)


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
  # list_display = ['id', 'user', 'first_name', 'last_name', 'phone_number', 'gender', 'role']
  list_display = [i.name for i in Profile._meta.fields]


@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
  # list_display = ['id', 'profile', 'speciality']
  list_display = [i.name for i in Speciality._meta.fields]


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
  # list_display = ['id', 'profile', 'speciality']
  list_display = [i.name for i in Doctor._meta.fields]


@admin.register(Assistant)
class AssistantAdmin(admin.ModelAdmin):
  # list_display = ['id', 'profile']
  list_display = [i.name for i in Assistant._meta.fields]


@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
  # list_display = ['id', 'name']
  list_display = [i.name for i in Disease._meta.fields]


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
  # list_display = ['id', 'name']
  list_display = [i.name for i in Habit._meta.fields]


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
  list_display = [i.name for i in Patient._meta.fields]


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
  list_display = [i.name for i in Case._meta.fields]


@admin.register(CaseChiefComplaint)
class CaseChiefComplaintAdmin(admin.ModelAdmin):
  list_display = [i.name for i in CaseChiefComplaint._meta.fields]


@admin.register(CaseFinding)
class CaseFindingAdmin(admin.ModelAdmin):
  list_display = [i.name for i in CaseFinding._meta.fields]


@admin.register(FindingImage)
class FindingImageAdmin(admin.ModelAdmin):
  list_display = [i.name for i in FindingImage._meta.fields]


@admin.register(CaseDocument)
class CaseDocumentAdmin(admin.ModelAdmin):
  list_display = [i.name for i in CaseDocument._meta.fields]


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
  list_display = [i.name for i in Prescription._meta.fields]


@admin.register(MedicineDoseType)
class MedicineDoseTypeAdmin(admin.ModelAdmin):
  list_display = [i.name for i in MedicineDoseType._meta.fields]


@admin.register(MedicineName)
class MedicineNameAdmin(admin.ModelAdmin):
  list_display = [i.name for i in MedicineName._meta.fields]


@admin.register(MedicineDoseQuantity)
class MedicineDoseQuantityAdmin(admin.ModelAdmin):
  list_display = [i.name for i in MedicineDoseQuantity._meta.fields]


@admin.register(MedicineDoseRegimen)
class MedicineDoseRegimenAdmin(admin.ModelAdmin):
  list_display = [i.name for i in MedicineDoseRegimen._meta.fields]


@admin.register(MedicineDoseDuration)
class MedicineDoseDurationAdmin(admin.ModelAdmin):
  list_display = [i.name for i in MedicineDoseDuration._meta.fields]


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
  list_display = [i.name for i in Medicine._meta.fields]


@admin.register(DietAdvice)
class DietAdviceAdmin(admin.ModelAdmin):
  list_display = [i.name for i in DietAdvice._meta.fields]
