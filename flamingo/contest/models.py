"""
:Created: 16 August 2015
:Author: Lucas Connors

"""

import datetime

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from photo.models import Photo


class Sponsor(models.Model):

    name = models.CharField(max_length=30, db_index=True)
    slug = models.SlugField(max_length=30, db_index=True)
    bio = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    def url(self):
        return reverse('sponsor_details', kwargs={'slug': self.slug})


class Contest(models.Model):

    sponsor = models.ForeignKey(Sponsor)
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    description = models.TextField(null=True, blank=True)
    submission_open = models.DateTimeField(null=True, blank=True)
    submission_close = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return "{sponsor}: {name}".format(
            sponsor=unicode(self.sponsor),
            name=self.name
        )

    def url(self):
        return reverse('contest_details', kwargs={'slug': self.slug})


@receiver(pre_save, sender=Contest)
def contest_pre_save(sender, instance, *args, **kwargs):
    if not instance.submission_open:
        instance.submission_open = timezone.now()
    if not instance.submission_close:
        instance.submission_close = instance.submission_open + \
            datetime.timedelta(days=7)
    if not instance.end:
        instance.end = instance.submission_close + datetime.timedelta(days=7)


class Entry(models.Model):

    contest = models.ForeignKey(Contest)
    photo = models.ForeignKey(Photo)

    class Meta:
        verbose_name_plural = "Entries"

    def __unicode__(self):
        return unicode(self.photo)
