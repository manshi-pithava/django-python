from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if not UserProfile.objects.filter(user=instance).exists():  # Prevent duplicate profiles
            role = 1 if instance.is_superuser else 2  # Superuser = Admin, Normal User = User
            UserProfile.objects.create(user=instance, role=role)
