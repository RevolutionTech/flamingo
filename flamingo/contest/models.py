"""
:Created: 16 August 2015
:Author: Lucas Connors

"""

import datetime

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone


class Sponsor(models.Model):

    name = models.CharField(max_length=30, db_index=True)
    bio = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class Contest(models.Model):

    sponsor = models.ForeignKey(Sponsor)
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(null=True, blank=True)
    submission_open = models.DateTimeField(null=True, blank=True)
    submission_close = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return "{sponsor}: {name}".format(
            sponsor=unicode(self.sponsor),
            name=self.name
        )


@receiver(pre_save, sender=Contest)
def contest_pre_save(sender, instance, *args, **kwargs):
    if not instance.submission_open:
        instance.submission_open = timezone.now()
    if not instance.submission_close:
        instance.submission_close = instance.submission_open + \
            datetime.timedelta(days=7)
    if not instance.end:
        instance.end = instance.submission_close + datetime.timedelta(days=7)
