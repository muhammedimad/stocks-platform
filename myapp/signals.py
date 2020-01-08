#__author__ = Mohammad Abdin
from .models import Profile
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

@receiver(post_save, sender = User)
def create_profile(sender, instance , created , **kwargs):
    """ here we want a user profile to be created automatically after an account is being created """
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender = User)
def save_profile(sender, instance , **kwargs):
    """
    receives the signal that askes for saving the profile
    :param sender: User Model
    :type sender: Model
    """
    instance.profile.save()
