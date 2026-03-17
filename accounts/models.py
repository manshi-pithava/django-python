from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    ROLE_CHOICES = (
        (1, "Admin"),
        (2, "User"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)  # ✅ Add phone field
    address = models.TextField(blank=True, null=True)  # ✅ Add address field
    role = models.IntegerField(choices=ROLE_CHOICES, default=2)  # Default role = User

    def __str__(self):
        return self.user.username

# ✅ Auto-create UserProfile when a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        role = 1 if instance.is_superuser else 2  # Superuser = Admin, Normal User = User
        UserProfile.objects.create(user=instance, phone="", address="", role=role)

# ✅ Auto-save UserProfile when User is updated
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

