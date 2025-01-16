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
  full_name = models.CharField(max_length=255, blank=True, null=True)
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


class Speciality(models.Model):
  title = models.CharField(max_length=320, unique=True)
  description = models.TextField(blank=True, null=True)
  is_active = models.BooleanField(default=True)
  # created_at = models.DateTimeField(default=datetime.now)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects = ActiveManager()
  admin_objects = AdminManager()

  def __str__(self):
    return f"Speciality<{self.title}>"


class Doctor(models.Model):
  profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
  degree = models.TextField(blank=True, null=True)
  speciality = models.ForeignKey(Speciality, on_delete=models.SET_NULL, blank=True, null=True)
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
  # blood_pressure = models.CharField(max_length=200, null=True, blank=True)
  # pulse = models.CharField(max_length=200, null=True, blank=True)
  # oxygen = models.CharField(max_length=200, null=True, blank=True)
  # body_temperature = models.FloatField(null=True, blank=True)
  # weight = models.FloatField(null=True, blank=True)
  # note_on_vitals = models.TextField(blank=True, null=True)
  diseases = models.ManyToManyField(Disease, blank=True, related_name="patients")
  other_diseases = models.TextField(blank=True, null=True)
  habits = models.ManyToManyField(Habit, blank=True, related_name="patients")
  other_habits = models.TextField(blank=True, null=True)
  created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
  doctors = models.ManyToManyField(Doctor, blank=True, related_name="patients")
  is_active = models.BooleanField(default=True)
  # created_at = models.DateTimeField(default=datetime.now)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects = ActiveManager()
  admin_objects = AdminManager()

  def __str__(self):
    return f"Patient<({self.id}) {self.full_name} ({self.phone_number})>"


class Case(models.Model):
  PAST_TREATMENT_CHOICES = [
    ('YES', 'Yes'),
    ('NO', 'No'),
  ]

  COMPLAINT_SEVERITY_CHOICES = [
    ('MILD', 'Mild'),
    ('MODERATE', 'Moderate'),
    ('SEVERE', 'Severe'),
  ]

  TREATMENT_LOCATION_CHOICES = [
    ('VILLAGE_RMP', 'Village RMP'),
    ('TOWN_RMP', 'Town RMP'),
    ('CITY_SPECIALIST', 'City Specialist'),
  ]

  TREATMENT_TYPE_CHOICES = [
    ('ORAL_MEDICINES', 'Only Oral Medicines'),
    ('IV_IM_DRIP', 'Only IV/IM/Drip'),
    ('BOTH_ORAL_IV_IM_DRIP', 'Both Oral & IV/IM/Drip'),
  ]

  patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
  assigned_doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, blank=True, null=True)
  blood_pressure_low = models.CharField(max_length=200, null=True, blank=True)
  blood_pressure_high = models.CharField(max_length=200, null=True, blank=True)
  blood_sugar_level = models.CharField(max_length=200, null=True, blank=True)
  pulse = models.CharField(max_length=200, null=True, blank=True)
  oxygen = models.CharField(max_length=200, null=True, blank=True)
  body_temperature = models.FloatField(null=True, blank=True)
  weight = models.FloatField(null=True, blank=True)
  note_on_vitals = models.TextField(blank=True, null=True)
  complaint_severity = models.CharField(max_length=20, choices=COMPLAINT_SEVERITY_CHOICES, blank=True, null=True)
  past_treatment = models.CharField(max_length=3, choices=PAST_TREATMENT_CHOICES, blank=True, null=True)
  treatment_location = models.CharField(max_length=50, choices=TREATMENT_LOCATION_CHOICES, blank=True, null=True)
  treatment_type = models.CharField(max_length=50, choices=TREATMENT_TYPE_CHOICES, blank=True, null=True)
  note = models.TextField(blank=True, null=True)
  follow_up_id = models.PositiveBigIntegerField(blank=True, null=True)
  follow_up_date = models.DateTimeField(blank=True, null=True)
  is_completed = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  # created_at = models.DateTimeField(default=datetime.now)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects = ActiveManager()
  admin_objects = AdminManager()

  def __str__(self):
    return f"Case<({self.id}) {self.patient.full_name} ({self.created_at})>"


class CaseChiefComplaint(models.Model):
  DURATION_UNIT_CHOICES = [
    ('DAY', 'Day'),
    # ('WEEK', 'Week'),
  ]

  # SEVERITY_CHOICES = [
  #   ('MILD', 'Mild'),
  #   ('MODERATE', 'Moderate'),
  #   ('SEVERE', 'Severe'),
  # ]

  case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="chief_complaints")
  title = models.CharField(max_length=255, blank=True, null=True)
  # severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, blank=True, null=True)
  duration = models.PositiveIntegerField(blank=True, null=True)
  duration_unit = models.CharField(max_length=5, choices=DURATION_UNIT_CHOICES, blank=True, null=True)
  is_active = models.BooleanField(default=True)
  # created_at = models.DateTimeField(default=datetime.now)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects = ActiveManager()
  admin_objects = AdminManager()

  def __str__(self):
    return f"CaseChiefComplaint<{self.title} ({self.severity} - {self.duration} {self.duration_unit})>"


class CaseFinding(models.Model):
  SEVERITY_CHOICES = [
    ('LOW', 'Low'),
    ('HIGH', 'High'),
  ]

  case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="findings")
  title = models.CharField(max_length=255, blank=True, null=True)
  severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
  is_active = models.BooleanField(default=True)
  # created_at = models.DateTimeField(default=datetime.now)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects = ActiveManager()
  admin_objects = AdminManager()

  def __str__(self):
    return f"CaseFinding<({self.id}) {self.title}>"


class FindingImage(models.Model):
  case_finding = models.ForeignKey(CaseFinding, on_delete=models.CASCADE, related_name="finding_images", null=True)
  file_name = models.CharField(max_length=255, blank=True, null=True)
  file_extension = models.CharField(max_length=10, blank=True, null=True)
  uploaded_file_name = models.CharField(max_length=512, blank=True, null=True)
  file_url = models.URLField(blank=True, null=True)
  is_active = models.BooleanField(default=True)
  # created_at = models.DateTimeField(default=datetime.now)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects = ActiveManager()
  admin_objects = AdminManager()

  def __str__(self):
    return f"FindingImage<{self.file_name}.{self.file_extension} ({self.file_url})>"


class CaseDocument(models.Model):
  DOCUMENT_SECTION_CHOICES = [
    ('MEDICINE_PHOTO', 'Medicine Photo'),
    ('LAB_REPORT', 'Lab Report'),
    ('PHOTO', 'Photo'),
  ]

  case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="documents")
  file_name = models.CharField(max_length=255, blank=True, null=True)
  file_extension = models.CharField(max_length=10, blank=True, null=True)
  uploaded_file_name = models.CharField(max_length=512, blank=True, null=True)
  file_url = models.URLField(blank=True, null=True)
  document_section = models.CharField(max_length=60, choices=DOCUMENT_SECTION_CHOICES, blank=True, null=True)
  is_active = models.BooleanField(default=True)
  # created_at = models.DateTimeField(default=datetime.now)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects = ActiveManager()
  admin_objects = AdminManager()

  def __str__(self):
    return f"CaseDocument<{self.file_name}.{self.file_extension} ({self.file_url})>"
