"""
:Created: 16 August 2015
:Author: Lucas Connors

"""

import datetime

from django.utils import timezone

from flamingo.tests import FlamingoTestCase
from contest.models import Sponsor, Contest


class SponsorTestCase(FlamingoTestCase):

    def testCreateSponsor(self):
        Sponsor.objects.all().delete()
        Sponsor.objects.create(name=self.CREATED_SPONSOR_NAME)
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


class HomeWebTestCase(FlamingoTestCase):

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
