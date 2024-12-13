from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from .models import Profile, Doctor, Assistant
from datetime import datetime


@receiver(post_save, sender=User)
def create_or_update_profile_from_user(sender, instance, created, **kwargs):
  if created:
    Profile.objects.create(
      user=instance,
      email=instance.email,
      role="ADMIN"
    )
    print(f"CREATED: {instance}, {type(instance)} ({created})")
    pass
  else:
    profile = Profile.objects.get(user=instance)
    print(f"profile: {profile}")
    profile.first_name = instance.first_name
    profile.last_name = instance.last_name
    profile.email = instance.email
    profile.save()
    print(f"UPDATED: {instance}, {type(instance)} ({created})")
    pass


@receiver(post_save, sender=Profile)
def create_or_update_doctor_or_assistant(sender, instance, created, **kwargs):
    if instance.role == 'DOCTOR':
        # Check if the doctor already exists
        doctor, doctor_created = Doctor.objects.get_or_create(profile=instance)
        if not doctor_created:
            # Update fields if necessary
            doctor.updated_at = datetime.now()
            doctor.save()
            print(f"DOCTOR UPDATED: {instance}, {type(instance)} ({created})")
        else:
            print(f"DOCTOR CREATED: {instance}, {type(instance)} ({created})")
    elif instance.role == 'ASSISTANT':
        # Check if the assistant already exists
        assistant, assistant_created = Assistant.objects.get_or_create(profile=instance)
        if not assistant_created:
            # Update fields if necessary
            assistant.updated_at = datetime.now()
            assistant.save()
            print(f"ASSISTANT UPDATED: {instance}, {type(instance)} ({created})")
        else:
            print(f"ASSISTANT CREATED: {instance}, {type(instance)} ({created})")