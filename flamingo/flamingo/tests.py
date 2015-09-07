"""
:Created: 6 September 2015
:Author: Lucas Connors

"""

import datetime

from django.contrib.auth.models import User
from django.test import Client, TestCase, TransactionTestCase
import pytz

from users.models import UserProfile
from contest.models import Sponsor, Contest


class FlamingoBaseTestCase(object):

    USER_USERNAME = 'jsmith'
    USER_EMAIL = 'jsmith@example.com'
    USER_PASSWORD = 'abc123'
    USER_PROFILE_BIO = 'I love photography.'
    CREATED_USER_USERNAME = 'CreatedUser'
    CREATED_USER_EMAIL = 'created@example.com'
    CREATED_USER_FIRST_NAME = 'Created'
    CREATED_USER_LAST_NAME = 'User'

    SPONSOR_NAME = 'Super Sponsor'
    SPONSOR_SLUG = 'super-sponsor'
    SPONSOR_BIO = 'We love photography.'
    CREATED_SPONSOR_NAME = 'Created Sponsor'
    CREATED_SPONSOR_SLUG = 'created-sponsor'

    CONTEST_NAME = 'Contest XYZ'
    CONTEST_SLUG = 'contest-xyz'
    CONTEST_DESCRIPTION = 'Are you a master of photography? Show us!'
    CONTEST_SUBMISSION_OPEN = datetime.datetime(2015, 1, 3, tzinfo=pytz.utc)
    CONTEST_SUBMISSION_CLOSE = datetime.datetime(2015, 1, 17, tzinfo=pytz.utc)
    CONTEST_END = datetime.datetime(2015, 1, 31, tzinfo=pytz.utc)
    CREATED_CONTEST_NAME = 'Created Contest'
    CREATED_CONTEST_SLUG = 'created-contest'
    CREATED_CONTEST_DESCRIPTION = 'This is a created contest.'

    def setUp(self):
        super(FlamingoBaseTestCase, self).setUp()
        self.client = Client()
        self.user_profile = UserProfile.objects.create_account(
            username=self.USER_USERNAME,
            email=self.USER_EMAIL,
            password=self.USER_PASSWORD
        )
        self.sponsor = Sponsor.objects.create(
            name=self.SPONSOR_NAME,
            slug=self.SPONSOR_SLUG
        )
        self.contest = Contest.objects.create(
            sponsor=self.sponsor,
            name=self.CONTEST_NAME,
            slug=self.CONTEST_SLUG,
            description=self.CONTEST_DESCRIPTION,
            submission_open=self.CONTEST_SUBMISSION_OPEN,
            submission_close=self.CONTEST_SUBMISSION_CLOSE,
            end=self.CONTEST_END
        )
        self.client.login(
            username=self.USER_USERNAME,
            password=self.USER_PASSWORD
        )

    def tearDown(self):
        Contest.objects.all().delete()
        Sponsor.objects.all().delete()
        UserProfile.objects.all().delete()
        User.objects.all().delete()
        super(FlamingoBaseTestCase, self).tearDown()


class FlamingoTestCase(FlamingoBaseTestCase, TestCase):
    pass


class FlamingoTransactionTestCase(FlamingoBaseTestCase, TransactionTestCase):
    pass
