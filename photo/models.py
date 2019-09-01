"""
:Created: 15 August 2015
:Author: Lucas Connors

"""

import os

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver

from users.models import UserProfile


class Photo(models.Model):

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    img = models.ImageField(upload_to="photo")
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


@receiver(post_delete, sender=Photo)
def user_profile_delete(sender, instance, *args, **kwargs):
    media_file_path = instance.img.file.name
    os.remove(media_file_path)
