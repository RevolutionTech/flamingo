"""
:Created: 15 August 2015
:Author: Lucas Connors

"""

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver

from users.managers import UserProfileManager


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)

    objects = UserProfileManager()

    def __str__(self):
        return str(self.user)

    def full_name(self):
        return u"{first} {last}".format(
            first=self.user.first_name, last=self.user.last_name
        ).strip()


@receiver(post_delete, sender=UserProfile)
def user_profile_delete(sender, instance, *args, **kwargs):
    instance.user.delete()
