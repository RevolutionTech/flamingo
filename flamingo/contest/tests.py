"""
:Created: 16 August 2015
:Author: Lucas Connors

"""

import datetime

from django.test import override_settings
from django.utils import timezone

from flamingo.tests import FlamingoTestCase
from contest.models import Sponsor, Contest, Entry, Vote


class SponsorTestCase(FlamingoTestCase):

    def testCreateSponsor(self):
        Sponsor.objects.all().delete()
        Sponsor.objects.create(
            name=self.CREATED_SPONSOR_NAME,
            slug=self.CREATED_SPONSOR_SLUG
        )
        self.assertEquals(Sponsor.objects.all().count(), 1)
        sponsor = Sponsor.objects.get()
        sponsor.bio = self.SPONSOR_BIO
        self.assertEquals(unicode(sponsor), self.CREATED_SPONSOR_NAME)
        self.assertEquals(sponsor.name, self.CREATED_SPONSOR_NAME)
        self.assertEquals(sponsor.bio, self.SPONSOR_BIO)


class ContestTestCase(FlamingoTestCase):

    def testCreateContest(self):
        Contest.objects.all().delete()
        Contest.objects.create(
            sponsor=self.sponsor,
            name=self.CREATED_CONTEST_NAME,
            slug=self.CREATED_CONTEST_SLUG,
            description=self.CREATED_CONTEST_DESCRIPTION,
            submission_open=self.YESTERDAY,
            submission_close=self.NEXT_WEEK,
            end=self.IN_TWO_WEEKS
        )
        self.assertEquals(Contest.objects.all().count(), 1)
        contest = Contest.objects.get()
        self.assertEquals(
            unicode(contest),
            "{sponsor}: {name}".format(
                sponsor=self.sponsor.name,
                name=self.CREATED_CONTEST_NAME
            )
        )
        self.assertEquals(contest.sponsor, self.sponsor)
        self.assertEquals(contest.name, self.CREATED_CONTEST_NAME)
        self.assertEquals(
            contest.description,
            self.CREATED_CONTEST_DESCRIPTION
        )

    def testCreateContestWithoutDates(self):
        contest = Contest.objects.create(
            sponsor=self.sponsor,
            name=self.CREATED_CONTEST_NAME,
            description=self.CREATED_CONTEST_DESCRIPTION
        )
        self.assertEquals(
            contest.submission_open.date(),
            timezone.now().date()
        )
        self.assertEquals(
            contest.submission_close,
            contest.submission_open + datetime.timedelta(days=7)
        )
        self.assertEquals(
            contest.end,
            contest.submission_close + datetime.timedelta(days=7)
        )


class EntryTestCase(FlamingoTestCase):

    def testCreateEntry(self):
        Entry.objects.all().delete()
        Entry.objects.create(
            contest=self.contest,
            photo=self.photo
        )
        self.assertEquals(Entry.objects.all().count(), 1)
        entry = Entry.objects.get()
        self.assertEquals(
            unicode(entry),
            unicode(entry.photo)
        )
        self.assertEquals(entry.contest, self.contest)
        self.assertEquals(entry.photo, self.photo)


class VoteTestCase(FlamingoTestCase):

    def testCreateUpvote(self):
        Vote.objects.all().delete()
        Vote.objects.create(
            entry=self.entry,
            user=self.user,
            vote_type=Vote.UPVOTE
        )
        self.assertEquals(Vote.objects.all().count(), 1)
        vote = Vote.objects.get()
        self.assertEquals(
            unicode(vote),
            'Upvote by {user} for {entry}'.format(
                user=unicode(self.user),
                entry=unicode(self.entry)
            )
        )

    def testCreateDownvote(self):
        Vote.objects.all().delete()
        Vote.objects.create(
            entry=self.entry,
            user=self.user,
            vote_type=Vote.DOWNVOTE
        )
        self.assertEquals(Vote.objects.all().count(), 1)
        vote = Vote.objects.get()
        self.assertEquals(
            unicode(vote),
            'Downvote by {user} for {entry}'.format(
                user=unicode(self.user),
                entry=unicode(self.entry)
            )
        )

    def testUserCannotUpvoteTwice(self):
        Vote.objects.all().delete()
        self.assertEquals(self.entry.vote_count(), 0)
        vote_count = self.entry.upvote(user=self.user)
        self.assertEquals(vote_count, 1)
        vote_count = self.entry.upvote(user=self.user)
        self.assertEquals(vote_count, 1)

    def testUserCannotDownvoteTwice(self):
        Vote.objects.all().delete()
        self.assertEquals(self.entry.vote_count(), 0)
        vote_count = self.entry.downvote(user=self.user)
        self.assertEquals(vote_count, -1)
        vote_count = self.entry.downvote(user=self.user)
        self.assertEquals(vote_count, -1)

    def testUserCanChangeVote(self):
        Vote.objects.all().delete()
        self.assertEquals(self.entry.vote_count(), 0)
        vote_count = self.entry.upvote(user=self.user)
        self.assertEquals(vote_count, 1)
        vote_count = self.entry.downvote(user=self.user)
        self.assertEquals(vote_count, -1)


class ContestAdminWebTestCase(FlamingoTestCase):

    def get_200s(self):
        return [
            '/admin/contest/',
            '/admin/contest/sponsor/',
            '/admin/contest/sponsor/add/',
            '/admin/contest/sponsor/{sponsor_id}/change/'.format(
                sponsor_id=self.sponsor.id
            ),
            '/admin/contest/contest/',
            '/admin/contest/contest/add/',
            '/admin/contest/contest/{contest_id}/change/'.format(
                contest_id=self.contest.id
            ),
            '/admin/contest/entry/',
            '/admin/contest/entry/add/',
            '/admin/contest/entry/{entry_id}/change/'.format(
                entry_id=self.entry.id
            ),
        ]


class HomeWebTestCase(FlamingoTestCase):

    def get_200s(self):
        return [
            '/',
        ]

    def testHomePageRenders(self):
        self.client.logout()
        self.assertResponseRenders('/')


class SponsorDetailsWebTestCase(FlamingoTestCase):

    def setUp(self):
        super(SponsorDetailsWebTestCase, self).setUp()
        self.sponsor_details_url = '/sponsor/details/{sponsor_slug}'.format(
            sponsor_slug=self.sponsor.slug
        )

    def get_200s(self):
        return [
            self.sponsor_details_url,
        ]

    def testSponsorDetailsPageRenders(self):
        self.client.logout()
        self.assertResponseRenders(self.sponsor_details_url)


class ContestDetailsWebTestCase(FlamingoTestCase):

    def setUp(self):
        super(ContestDetailsWebTestCase, self).setUp()
        self.contest_details_url = '/contest/details/{contest_slug}'.format(
            contest_slug=self.contest.slug
        )

    def testContestDetailsPageRenders(self):
        response = self.assertResponseRenders(self.contest_details_url)
        selectors = [
            'dropzone-submit-photo',
            'upvote-button',
            'downvote-button',
        ]
        for selector in selectors:
            self.assertIn(selector, response.content)
        self.assertNotIn('login-to-vote', response.content)

    def testUnauthenticatedCannotVoteOrUpload(self):
        self.client.logout()
        response = self.assertResponseRenders(self.contest_details_url)
        selectors = [
            'dropzone-submit-photo',
            'upvote-button',
            'downvote-button',
        ]
        for selector in selectors:
            self.assertNotIn(selector, response.content)
        self.assertIn('login-to-vote', response.content)


class ContestUploadPhotoTestCase(FlamingoTestCase):

    PHOTO_FILENAME = 'jsmith.jpg'
    PHOTO_NONIMAGE_FILENAME = 'nonimage.jpg'

    def setUp(self):
        super(ContestUploadPhotoTestCase, self).setUp()
        self.contest_upload_url = '/contest/upload/{contest_slug}'.format(
            contest_slug=self.contest.slug
        )
        self.ended_contest_upload_url = '/contest/upload/{contest_slug}'.format(
            contest_slug=self.ended_contest.slug
        )

    def testSuccessfulUpload(self):
        image = self.create_test_image(filename=self.PHOTO_FILENAME)
        self.assertResponseRenders(self.contest_upload_url, status_code=205, method='POST', data={'image': image,})

    def testRejectUnauthenticatedUsers(self):
        self.client.logout()
        image = self.create_test_image(filename=self.PHOTO_FILENAME)
        self.assertResponseRenders(self.contest_upload_url, status_code=401, method='POST', data={'image': image,})

    def testRejectInvalidContest(self):
        invalid_contest_upload_url = '/contest/upload/{contest_slug}'.format(
            contest_slug='nonexistent-contest'
        )
        image = self.create_test_image(filename=self.PHOTO_FILENAME)
        self.assertResponseRenders(invalid_contest_upload_url, status_code=404, method='POST', data={'image': image,})

    # For this test, set the maximum image size to 5 bytes
    @override_settings(MAXIMUM_IMAGE_SIZE=5)
    def testRejectLargePhotos(self):
        image = self.create_test_image(filename=self.PHOTO_FILENAME)
        self.assertResponseRenders(self.contest_upload_url, status_code=400, method='POST', data={'image': image,})

    def testRejectNonImages(self):
        image = self.create_test_image(filename=self.PHOTO_NONIMAGE_FILENAME)
        self.assertResponseRenders(self.contest_upload_url, status_code=400, method='POST', data={'image': image,})

    def testRejectSubmissionAfterEndSubmissionDate(self):
        image = self.create_test_image(filename=self.PHOTO_FILENAME)
        self.assertResponseRenders(self.ended_contest_upload_url, status_code=400, method='POST', data={'image': image,})


class ContestVoteEntryTestCase(FlamingoTestCase):

    def testSuccessfulUpvote(self):
        contest_upvote_url = \
            '/contest/details/{contest_slug}/entry/{entry_id}/upvote/'.format(
                contest_slug=self.contest.slug,
                entry_id=self.entry.id
            )
        self.assertResponseRenders(contest_upvote_url, method='POST')

    def testSuccessfulDownvote(self):
        contest_downvote_url = \
            '/contest/details/{contest_slug}/entry/{entry_id}/downvote/'.format(
                contest_slug=self.contest.slug,
                entry_id=self.entry.id
            )
        self.assertResponseRenders(contest_downvote_url, method='POST')

    def testRejectUnauthenticatedUsers(self):
        self.client.logout()
        contest_upvote_url = \
            '/contest/details/{contest_slug}/entry/{entry_id}/upvote/'.format(
                contest_slug=self.contest.slug,
                entry_id=self.entry.id
            )
        self.assertResponseRenders(contest_upvote_url, status_code=401, method='POST')

    def testRejectInvalidContest(self):
        contest_upvote_url = \
            '/contest/details{contest_slug}/entry/{entry_id}/upvote/'.format(
                contest_slug='nonexistent-contest',
                entry_id=self.entry.id
            )
        self.assertResponseRenders(contest_upvote_url, status_code=404, method='POST')

    def testRejectInvalidEntry(self):
        contest_upvote_url = \
            '/contest/details/{contest_slug}/entry/{entry_id}/upvote/'.format(
                contest_slug=self.contest.slug,
                entry_id=Entry.objects.all().order_by('-id')[0].id + 1
            )
        self.assertResponseRenders(contest_upvote_url, status_code=404, method='POST')

    def testRejectNonMatchingEntry(self):
        new_contest = Contest.objects.create(
            sponsor=self.sponsor,
            name=self.CREATED_CONTEST_NAME,
            slug=self.CREATED_CONTEST_SLUG,
            description=self.CREATED_CONTEST_DESCRIPTION,
            submission_open=self.YESTERDAY,
            submission_close=self.NEXT_WEEK,
            end=self.IN_TWO_WEEKS
        )
        _, new_photo = self.create_test_photo(
            self.user_profile,
            'New photo',
            self.CREATED_PHOTO_FILENAME,
            self.CREATED_PHOTO_DESCRIPTION
        )
        new_entry = Entry.objects.create(contest=new_contest, photo=new_photo)
        contest_upvote_url = \
            '/contest/details/{contest_slug}/entry/{entry_id}/upvote/'.format(
                contest_slug=self.contest.slug,
                entry_id=new_entry.id
            )
        self.assertResponseRenders(contest_upvote_url, status_code=404, method='POST')

    def testRejectVotingAfterEndDate(self):
        _, photo = self.create_test_photo(
            self.user_profile,
            'Photo',
            self.CREATED_PHOTO_FILENAME,
            self.CREATED_PHOTO_DESCRIPTION
        )
        entry = Entry.objects.create(contest=self.ended_contest, photo=photo)
        contest_upvote_url = \
            '/contest/details/{contest_slug}/entry/{entry_id}/upvote/'.format(
                contest_slug=self.ended_contest.slug,
                entry_id=entry.id
            )
        self.assertResponseRenders(contest_upvote_url, status_code=400, method='POST')
