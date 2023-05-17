import uuid

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile
from contracts.models import Contracts

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        up = UserProfile.objects.create(user=instance)
        up.showing_contracts.set(Contracts.objects.filter(show_to_all=True))
        up.ref_link = str(uuid.uuid4())[:6]


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
