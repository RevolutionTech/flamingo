"""
:Created: 16 August 2015
:Author: Lucas Connors

"""

import datetime

from django.test import TestCase
from django.utils import timezone
import pytz

from contest.models import Sponsor, Contest


class SponsorTestCase(TestCase):

    SPONSOR_NAME = 'Super Sponsor'
    SPONSOR_BIO = 'We love photography.'
    CREATED_SPONSOR_NAME = 'Created Sponsor'

    def setUp(self):
        super(SponsorTestCase, self).setUp()
        self.sponsor = Sponsor.objects.create(name=self.SPONSOR_NAME)

    def tearDown(self):
        Sponsor.objects.all().delete()
        super(SponsorTestCase, self).tearDown()

    def testCreateSponsor(self):
        Sponsor.objects.all().delete()
        Sponsor.objects.create(name=self.CREATED_SPONSOR_NAME)
        self.assertEquals(Sponsor.objects.all().count(), 1)
        sponsor = Sponsor.objects.get()
        sponsor.bio = self.SPONSOR_BIO
        self.assertEquals(sponsor.name, self.CREATED_SPONSOR_NAME)
        self.assertEquals(sponsor.bio, self.SPONSOR_BIO)


class ContestTestCase(TestCase):

    SPONSOR_NAME = 'Super Sponsor'
    CONTEST_NAME = 'Contest XYZ'
    CONTEST_DESCRIPTION = 'Are you a master of photography? Show us!'
    CONTEST_SUBMISSION_OPEN = datetime.datetime(2015, 1, 3, tzinfo=pytz.utc)
    CONTEST_SUBMISSION_CLOSE = datetime.datetime(2015, 1, 17, tzinfo=pytz.utc)
    CONTEST_END = datetime.datetime(2015, 1, 31, tzinfo=pytz.utc)
    CREATED_CONTEST_NAME = 'Created Contest'
    CREATED_CONTEST_DESCRIPTION = 'This is a created contest.'

    def setUp(self):
        super(ContestTestCase, self).setUp()
        self.sponsor = Sponsor.objects.create(name=self.SPONSOR_NAME)
        self.contest = Contest.objects.create(
            sponsor=self.sponsor,
            name=self.CONTEST_NAME,
            description=self.CONTEST_DESCRIPTION,
            submission_open=self.CONTEST_SUBMISSION_OPEN,
            submission_close=self.CONTEST_SUBMISSION_CLOSE,
            end=self.CONTEST_END
        )

    def tearDown(self):
        Sponsor.objects.all().delete()
        super(ContestTestCase, self).tearDown()

    def testCreateContest(self):
        Contest.objects.all().delete()
        Contest.objects.create(
            sponsor=self.sponsor,
            name=self.CREATED_CONTEST_NAME,
            description=self.CREATED_CONTEST_DESCRIPTION,
            submission_open=self.CONTEST_SUBMISSION_OPEN,
            submission_close=self.CONTEST_SUBMISSION_CLOSE,
            end=self.CONTEST_END
        )
        self.assertEquals(Contest.objects.all().count(), 1)
        contest = Contest.objects.get()
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
