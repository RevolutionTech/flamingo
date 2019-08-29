"""
:Created: 16 August 2015
:Author: Lucas Connors

"""

import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone

from photo.models import Photo


class Sponsor(models.Model):

    name = models.CharField(max_length=30, db_index=True)
    slug = models.SlugField(max_length=30, db_index=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def url(self):
        return reverse('sponsor_details', kwargs={'slug': self.slug})


class Contest(models.Model):

    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    description = models.TextField(null=True, blank=True)
    submission_open = models.DateTimeField(null=True, blank=True)
    submission_close = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "{sponsor}: {name}".format(
            sponsor=str(self.sponsor),
            name=self.name
        )

    def url(self):
        return reverse('contest_details', kwargs={'slug': self.slug})

    def upload_photo_url(self):
        return reverse('contest_upload_photo', kwargs={'slug': self.slug})


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

    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Entries"

    def __str__(self):
        return str(self.photo)

    def vote_count(self):
        votes = Vote.objects.filter(entry=self)
        num_upvotes = votes.filter(vote_type=Vote.UPVOTE).count()
        num_downvotes = votes.filter(vote_type=Vote.DOWNVOTE).count()
        return num_upvotes - num_downvotes

    def vote(self, user, vote_type):
        Vote.objects.update_or_create(
            entry=self,
            user=user,
            defaults={'vote_type': vote_type}
        )
        return self.vote_count()

    def has_voted(self, user, vote_type):
        return Vote.objects.filter(
            entry=self,
            user=user,
            vote_type=vote_type
        ).exists()

    def upvote(self, user):
        return self.vote(user, Vote.UPVOTE)

    def has_upvoted(self, user):
        return self.has_voted(user, Vote.UPVOTE)

    def downvote(self, user):
        return self.vote(user, Vote.DOWNVOTE)

    def has_downvoted(self, user):
        return self.has_voted(user, Vote.DOWNVOTE)


class Vote(models.Model):
    DOWNVOTE = 0
    UPVOTE = 1
    VOTE_CHOICES = (
        (DOWNVOTE, 'Downvote'),
        (UPVOTE, 'Upvote'),
    )

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_type = models.PositiveSmallIntegerField(
        choices=VOTE_CHOICES,
        db_index=True
    )

    class Meta:
        unique_together = (('entry', 'user',),)

    def __str__(self):
        return "{vote_type} by {user} for {entry}".format(
            vote_type=self.get_vote_type_display(),
            entry=str(self.entry),
            user=str(self.user)
        )
