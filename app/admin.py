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
  CaseDocument
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
