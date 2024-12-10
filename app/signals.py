from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from .models import Profile, Doctor, Assistant


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
def create_doctor_or_assistant_from_profile(sender, instance, created, **kwargs):
  if not created:
    if instance.role == 'DOCTOR':
      Doctor.objects.create(profile=instance)
      print(f"DOCTOR CREATED: {instance}, {type(instance)} ({created})")
    elif instance.role == 'ASSISTANT':
      Assistant.objects.create(profile=instance)
      print(f"ASSISTANT CREATED: {instance}, {type(instance)} ({created})")
    
    pass
