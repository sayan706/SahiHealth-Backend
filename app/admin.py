from django.contrib import admin
from .models import Profile, Doctor, Assistant, Disease, Habit, Patient


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
  # list_display = ['id', 'user', 'first_name', 'last_name', 'phone_number', 'gender', 'role']
  list_display = [i.name for i in Profile._meta.fields]


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
