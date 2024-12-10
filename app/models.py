from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from .model_manager import ActiveManager, AdminManager


def profile_picture_path(instance, filename):
  return f"profile_pictures/{instance.role}/{filename}"


# Create your models here.
class Profile(models.Model):
  ROLE_CHOICES = [
    ('ADMIN', 'Admin'),
    ('DOCTOR', 'Doctor'),
    ('ASSISTANT', 'Assistant'),
  ]
  GENDER_CHOICES = [
    ('MALE', 'Male'),
    ('FEMALE', 'Female'),
    ('OTHER', 'Other'),
  ]

  user = models.OneToOneField(User, on_delete=models.CASCADE)
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  email = models.EmailField(max_length=200, unique=True, null=True, blank=True)
  phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
  gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
  location = models.CharField(max_length=255, blank=True, null=True)
  profile_picture = models.ImageField(upload_to=profile_picture_path, blank=True, null=True)
  role = models.CharField(max_length=10, choices=ROLE_CHOICES)
  is_active = models.BooleanField(default=True)
  # created_at = models.DateTimeField(auto_now_add=True)
  created_at = models.DateTimeField(default=datetime.now)
  updated_at = models.DateTimeField(null=True, blank=True)

  objects = ActiveManager()
  admin_objects = AdminManager()

  def __str__(self):
    return f"Profile<{self.user.username} ({self.role})>"


class Doctor(models.Model):
  profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
  speciality = models.CharField(max_length=100, blank=True, null=True)
  is_active = models.BooleanField(default=True)
  # created_at = models.DateTimeField(auto_now_add=True)
  created_at = models.DateTimeField(default=datetime.now)
  updated_at = models.DateTimeField(null=True, blank=True)

  objects = ActiveManager()
  admin_objects = AdminManager()

  def __str__(self):
    return f"Doctor<{self.profile.first_name} {self.profile.last_name} ({self.speciality})"


class Assistant(models.Model):
  profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
  is_active = models.BooleanField(default=True)
  # created_at = models.DateTimeField(auto_now_add=True)
  created_at = models.DateTimeField(default=datetime.now)
  updated_at = models.DateTimeField(null=True, blank=True)

  objects = ActiveManager()
  admin_objects = AdminManager()

  def __str__(self):
    return f"Assistant<{self.profile.user.username} ({self.profile.role})>"
