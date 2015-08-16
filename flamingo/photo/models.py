"""
:Created: 15 August 2015
:Author: Lucas Connors

"""

from django.db import models

from users.models import UserProfile


class Photo(models.Model):

    user_profile = models.ForeignKey(UserProfile)
    title = models.CharField(max_length=30)
    img = models.ImageField(upload_to='photo')
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.title
