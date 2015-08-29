"""
:Created: 16 August 2015
:Author: Lucas Connors

"""

import datetime

from django.test import Client, TestCase
from django.utils import timezone
import pytz

from contest.models import Sponsor, Contest
from users.models import UserProfile


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
        self.assertEquals(unicode(sponsor), self.CREATED_SPONSOR_NAME)
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


class HomeWebTestCase(TestCase):

    USER_USERNAME = 'jsmith'
    USER_EMAIL = 'jsmith@example.com'
    USER_PASSWORD = 'abc123'
    SPONSOR_NAME = 'Super Sponsor'
    CONTEST_NAME = 'Contest XYZ'
    CONTEST_DESCRIPTION = 'Are you a master of photography? Show us!'
    CONTEST_SUBMISSION_OPEN = datetime.datetime(2015, 1, 3, tzinfo=pytz.utc)
    CONTEST_SUBMISSION_CLOSE = datetime.datetime(2015, 1, 17, tzinfo=pytz.utc)
    CONTEST_END = datetime.datetime(2015, 1, 31, tzinfo=pytz.utc)
    CREATED_CONTEST_NAME = 'Created Contest'
    CREATED_CONTEST_DESCRIPTION = 'This is a created contest.'

    def setUp(self):
        super(HomeWebTestCase, self).setUp()
        self.client = Client()
        self.user_profile = UserProfile.objects.create_account(
            username=self.USER_USERNAME,
            email=self.USER_EMAIL,
            password=self.USER_PASSWORD
        )
        self.client.login(
            username=self.USER_USERNAME,
            password=self.USER_PASSWORD
        )
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
        Contest.objects.all().delete()
        Sponsor.objects.all().delete()
        super(HomeWebTestCase, self).tearDown()

    def testHomePageRenders(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def testRedirectsUnauthenticatedUsersToLogin(self):
        self.client.logout()
        response = self.client.get('/', follow=True)
        url, status_code = response.redirect_chain[0]
        self.assertEquals(status_code, 302)
        self.assertEquals(url, 'http://testserver/login/?next=/')

    def testOnlyActiveContestsShowOnHome(self):
        Contest.objects.all().delete()

        yesterday = timezone.now() - datetime.timedelta(days=1)
        next_week = yesterday + datetime.timedelta(days=7)
        next_week_1_day = next_week + datetime.timedelta(days=1)
        active_contest_name = 'Active contest'
        Contest.objects.create(
            sponsor=self.sponsor,
            name=active_contest_name,
            description=self.CONTEST_DESCRIPTION,
            submission_open=yesterday,
            submission_close=next_week,
            end=next_week_1_day
        )
        ended_contest_name = 'Ended contest'
        Contest.objects.create(
            sponsor=self.sponsor,
            name=ended_contest_name,
            description=self.CONTEST_DESCRIPTION,
            submission_open=yesterday - datetime.timedelta(days=21),
            submission_close=next_week - datetime.timedelta(days=21),
            end=next_week_1_day - datetime.timedelta(days=21)
        )

        response = self.client.get('/')
        self.assertTrue(active_contest_name in response.content)
        self.assertFalse(ended_contest_name in response.content)
