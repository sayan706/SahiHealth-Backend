from django.contrib import admin
from .models import Profile, Doctor, Assistant


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
  list_display = ['id', 'user', 'first_name', 'last_name', 'phone_number', 'gender', 'role']


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
  list_display = ['id', 'profile', 'speciality']


@admin.register(Assistant)
class AssistantAdmin(admin.ModelAdmin):
  list_display = ['id', 'profile']
