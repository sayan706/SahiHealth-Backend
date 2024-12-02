from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
  list_display = ["role_id", "name" , "uuid"]

@admin.register(DoctorsandCompunders)
class DoctorandCompundersAdmin(admin.ModelAdmin):
  list_display = ["name", "username","role","uuid"]


