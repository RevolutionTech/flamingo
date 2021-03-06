"""
:Created: 6 September 2015
:Author: Lucas Connors

"""

import datetime
import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from pigeon.test import RenderTestCase, RenderTransactionTestCase

from contest.models import Contest, Entry, Sponsor
from photo.models import Photo
from users.models import UserProfile


class FlamingoBaseTestCase:

    NOW = timezone.now()
    USER_USERNAME = "jsmith"
    USER_EMAIL = "jsmith@example.com"
    USER_PASSWORD = "abc123"
    USER_PROFILE_BIO = "I love photography."
    CREATED_USER_USERNAME = "CreatedUser"
    CREATED_USER_EMAIL = "created@example.com"
    CREATED_USER_FIRST_NAME = "Created"
    CREATED_USER_LAST_NAME = "User"

    TEST_PHOTOS_DIR = os.path.join(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
        "photo",
        "testphotos",
    )
    CREATED_PHOTO_FILENAME = "sunset.jpg"
    CREATED_PHOTO_TITLE = "Sunset"
    CREATED_PHOTO_DESCRIPTION = "A sunset."

    SPONSOR_NAME = "Super Sponsor"
    SPONSOR_SLUG = "super-sponsor"
    SPONSOR_BIO = "We love photography."
    CREATED_SPONSOR_NAME = "Created Sponsor"
    CREATED_SPONSOR_SLUG = "created-sponsor"

    CONTEST_NAME = "Contest XYZ"
    CONTEST_SLUG = "contest-xyz"
    CONTEST_DESCRIPTION = "Are you a master of photography? Show us!"
    ENDED_CONTEST_NAME = "Ended Contest XYZ"
    ENDED_CONTEST_SLUG = "ended-contest-xyz"
    TWO_WEEKS_AGO = NOW - datetime.timedelta(days=14)
    LAST_WEEK = NOW - datetime.timedelta(days=7)
    YESTERDAY = NOW - datetime.timedelta(days=1)
    NEXT_WEEK = NOW + datetime.timedelta(days=7)
    IN_TWO_WEEKS = NOW + datetime.timedelta(days=14)
    CREATED_CONTEST_NAME = "Created Contest"
    CREATED_CONTEST_SLUG = "created-contest"
    CREATED_CONTEST_DESCRIPTION = "This is a created contest."

    @classmethod
    def create_test_image(cls, filename):
        photo_full_filename = os.path.join(cls.TEST_PHOTOS_DIR, filename)
        try:
            image_content = open(photo_full_filename, "rb").read()
        except OSError:
            raise OSError(
                'Test photo "{filename}" missing or could not be read.'.format(
                    filename=filename
                )
            )
        return SimpleUploadedFile(
            name=filename, content=image_content, content_type="image/jpeg"
        )

    @classmethod
    def create_test_photo(cls, user_profile, title, filename, description):
        image = cls.create_test_image(filename)
        photo = Photo.objects.create(
            user_profile=user_profile, title=title, img=image, description=description
        )
        return image, photo

    def setup_user(self):
        self.user_profile = UserProfile.objects.create_account(
            username=self.USER_USERNAME,
            email=self.USER_EMAIL,
            password=self.USER_PASSWORD,
        )
        self.user = self.user_profile.user
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        self.client.login(username=self.USER_USERNAME, password=self.USER_PASSWORD)

    def create_first_instances(self):
        _, self.photo = self.create_test_photo(
            user_profile=self.user_profile,
            title=self.CREATED_PHOTO_TITLE,
            filename=self.CREATED_PHOTO_FILENAME,
            description=self.CREATED_PHOTO_DESCRIPTION,
        )
        self.sponsor = Sponsor.objects.create(
            name=self.SPONSOR_NAME, slug=self.SPONSOR_SLUG
        )
        self.contest = Contest.objects.create(
            sponsor=self.sponsor,
            name=self.CONTEST_NAME,
            slug=self.CONTEST_SLUG,
            description=self.CONTEST_DESCRIPTION,
            submission_open=self.YESTERDAY,
            submission_close=self.NEXT_WEEK,
            end=self.IN_TWO_WEEKS,
        )
        self.ended_contest = Contest.objects.create(
            sponsor=self.sponsor,
            name=self.ENDED_CONTEST_NAME,
            slug=self.ENDED_CONTEST_SLUG,
            description=self.CONTEST_DESCRIPTION,
            submission_open=self.TWO_WEEKS_AGO,
            submission_close=self.LAST_WEEK,
            end=self.YESTERDAY,
        )
        self.entry = Entry.objects.create(contest=self.contest, photo=self.photo)

    def setUp(self):
        super().setUp()
        self.setup_user()
        self.create_first_instances()


class FlamingoTestCase(FlamingoBaseTestCase, RenderTestCase):
    pass


class FlamingoTransactionTestCase(FlamingoBaseTestCase, RenderTransactionTestCase):
    pass


class FlamingoGeneralTestCase(FlamingoTestCase):
    def testCreateTestPhotoMissing(self):
        with self.assertRaises(IOError):
            self.create_test_image("missing.jpg")


class AdminWebTestCase(FlamingoTestCase):
    def get200s(self):
        return ["/admin/"]

    def testAdminLoginPageRenders(self):
        self.client.logout()
        self.assertResponseRedirects("/admin/", "/admin/login/")
