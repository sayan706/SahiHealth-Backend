# from datetime import datetime
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
  email = models.EmailField(max_length=320, unique=True, null=True, blank=True)
  phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
  gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
  location = models.TextField(blank=True, null=True)
  dp_url = models.URLField(blank=True, null=True)
  profile_picture = models.ImageField(upload_to=profile_picture_path, blank=True, null=True)
  role = models.CharField(max_length=10, choices=ROLE_CHOICES)
  is_active = models.BooleanField(default=True)
  # created_at = models.DateTimeField(default=datetime.now)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects = ActiveManager()
  admin_objects = AdminManager()

  def __str__(self):
    return f"Profile<{self.user.username} ({self.role})>"


class Doctor(models.Model):
  profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
  speciality = models.TextField(blank=True, null=True)
  is_active = models.BooleanField(default=True)
  # created_at = models.DateTimeField(default=datetime.now)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects = ActiveManager()
  admin_objects = AdminManager()

  def __str__(self):
    return f"Doctor<{self.profile.user.username} - {self.profile.first_name} {self.profile.last_name} ({self.speciality})>"


class Assistant(models.Model):
  profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
  is_active = models.BooleanField(default=True)
  # created_at = models.DateTimeField(default=datetime.now)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects = ActiveManager()
  admin_objects = AdminManager()

  def __str__(self):
    return f"Assistant<{self.profile.user.username} - {self.profile.first_name} {self.profile.last_name}>"


class Disease(models.Model):
  name = models.CharField(max_length=255, unique=True)
  is_active = models.BooleanField(default=True)
  # created_at = models.DateTimeField(default=datetime.now)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects = ActiveManager()
  admin_objects = AdminManager()

  def __str__(self):
    return f"Disease<{self.name} ({self.id})>"


class Habit(models.Model):
  name = models.CharField(max_length=255, unique=True)
  is_active = models.BooleanField(default=True)
  # created_at = models.DateTimeField(default=datetime.now)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects = ActiveManager()
  admin_objects = AdminManager()

  def __str__(self):
    return f"Habit<{self.name} ({self.id})>"


class Patient(models.Model):
  GENDER_CHOICES = [
    ('MALE', 'Male'),
    ('FEMALE', 'Female'),
    ('OTHER', 'Other'),
  ]

  full_name = models.CharField(max_length=255)
  phone_number = models.CharField(max_length=15, unique=True)
  gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
  age = models.CharField(max_length=255)
  address = models.TextField(blank=True, null=True)
  allergy = models.TextField(blank=True, null=True)
  blood_pressure = models.CharField(max_length=200, null=True, blank=True)
  pulse = models.CharField(max_length=200, null=True, blank=True)
  oxygen = models.CharField(max_length=200, null=True, blank=True)
  body_temperature = models.FloatField(null=True, blank=True)
  weight = models.FloatField(null=True, blank=True)
  note_on_vitals = models.TextField(blank=True, null=True)
  diseases = models.ManyToManyField(Disease, blank=True, related_name="patients")
  other_diseases = models.TextField(blank=True, null=True)
  habits = models.ManyToManyField(Habit, blank=True, related_name="patients")
  other_habits = models.TextField(blank=True, null=True)
  created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
  assigned_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
  is_active = models.BooleanField(default=True)
  # created_at = models.DateTimeField(default=datetime.now)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects = ActiveManager()
  admin_objects = AdminManager()

  def __str__(self):
    return f"Patient<{self.id} - {self.full_name} ({self.phone_number})>"
