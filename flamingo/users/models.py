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

    user = models.OneToOneField(User)
    bio = models.TextField(null=True, blank=True)

    objects = UserProfileManager()

    def __unicode__(self):
        return unicode(self.user)


@receiver(post_delete, sender=UserProfile)
def user_profile_delete(sender, instance, *args, **kwargs):
    instance.user.delete()
