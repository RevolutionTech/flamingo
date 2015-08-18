"""
:Created: 15 August 2015
:Author: Lucas Connors

"""

from django.contrib.auth.models import User
from django.db import transaction
from django.test import Client, TestCase, TransactionTestCase

from users.exceptions import UserAlreadyExistsException
from users.models import UserProfile


class UserTestCase(TransactionTestCase):

    USER_USERNAME = 'jsmith'
    USER_EMAIL = 'jsmith@example.com'
    USER_PASSWORD = 'abc123'
    USER_PROFILE_BIO = 'I love photography.'
    CREATED_USER_USERNAME = 'CreatedUser'
    CREATED_USER_EMAIL = 'created@example.com'
    CREATED_USER_FIRST_NAME = 'Created'
    CREATED_USER_LAST_NAME = 'User'

    def setUp(self):
        super(UserTestCase, self).setUp()
        self.user_profile = UserProfile.objects.create_account(
            username=self.USER_USERNAME,
            email=self.USER_EMAIL,
            password=self.USER_PASSWORD
        )

    def tearDown(self):
        UserProfile.objects.all().delete()
        User.objects.all().delete()
        super(UserTestCase, self).tearDown()

    def testCreateAccount(self):
        UserProfile.objects.all().delete()
        UserProfile.objects.create_account(
            username=self.CREATED_USER_USERNAME,
            email=self.CREATED_USER_EMAIL,
            password=self.USER_PASSWORD,
            first_name=self.CREATED_USER_FIRST_NAME,
            last_name=self.CREATED_USER_LAST_NAME,
        )
        self.assertEquals(User.objects.all().count(), 1)
        self.assertEquals(UserProfile.objects.all().count(), 1)
        created_user_profile = UserProfile.objects.get()
        created_user_profile.bio = self.USER_PROFILE_BIO
        self.assertEquals(
            unicode(created_user_profile),
            self.CREATED_USER_USERNAME
        )
        self.assertEquals(
            created_user_profile.user.username,
            self.CREATED_USER_USERNAME
        )
        self.assertEquals(
            created_user_profile.user.email,
            self.CREATED_USER_EMAIL
        )
        self.assertEquals(
            created_user_profile.user.first_name,
            self.CREATED_USER_FIRST_NAME
        )
        self.assertEquals(
            created_user_profile.user.last_name,
            self.CREATED_USER_LAST_NAME
        )
        self.assertEquals(
            created_user_profile.full_name(),
            "{first} {last}".format(
                first=self.CREATED_USER_FIRST_NAME,
                last=self.CREATED_USER_LAST_NAME
            )
        )
        self.assertEquals(
            created_user_profile.bio,
            self.USER_PROFILE_BIO
        )

    def testDeletedAccountAvailableAgain(self):
        self.user_profile.delete()
        UserProfile.objects.create_account(
            username=self.USER_USERNAME,
            email=self.USER_EMAIL,
            password=self.USER_PASSWORD
        )
        self.assertEquals(User.objects.all().count(), 1)
        self.assertEquals(UserProfile.objects.all().count(), 1)

    def testCannotCreateAccountWithTakenUsername(self):
        with self.assertRaises(UserAlreadyExistsException):
            UserProfile.objects.create_account(
                username=self.USER_USERNAME,
                email=self.CREATED_USER_EMAIL,
                password=self.USER_PASSWORD
            )

    def testCannotCreateAccountWithTakenEmail(self):
        with self.assertRaises(UserAlreadyExistsException):
            UserProfile.objects.create_account(
                username=self.CREATED_USER_USERNAME,
                email=self.USER_EMAIL,
                password=self.USER_PASSWORD
            )


class RegisterWebTestCase(TestCase):

    USER_USERNAME = 'jsmith'
    USER_EMAIL = 'jsmith@example.com'
    USER_PASSWORD = 'abc123'
    CREATED_USER_USERNAME = 'CreatedUser'
    CREATED_USER_EMAIL = 'created@example.com'
    CREATED_USER_FIRST_NAME = 'Created'
    CREATED_USER_LAST_NAME = 'User'

    def setUp(self):
        super(RegisterWebTestCase, self).setUp()
        self.client = Client()
        self.user_profile = UserProfile.objects.create_account(
            username=self.USER_USERNAME,
            email=self.USER_EMAIL,
            password=self.USER_PASSWORD
        )

    def testRegisterPageRenders(self):
        response = self.client.get('/register')
        self.assertEquals(response.status_code, 200)

    def testUserRegisters(self):
        UserProfile.objects.all().delete()
        self.client.get('/register')
        payload = {
            'username': self.CREATED_USER_USERNAME,
            'email': self.CREATED_USER_EMAIL,
            'password': self.USER_PASSWORD,
            'password_confirm': self.USER_PASSWORD,
            'first_name': self.CREATED_USER_FIRST_NAME,
            'last_name': self.CREATED_USER_LAST_NAME,
        }
        response = self.client.post('/register', payload, follow=True)
        url, status_code = response.redirect_chain[0]
        self.assertEquals(status_code, 302)
        self.assertEquals(url, 'http://testserver/')
        self.assertEquals(UserProfile.objects.all().count(), 1)

    def testRedirectsAuthenticatedUsersToHome(self):
        self.client.login(
            username=self.USER_USERNAME,
            password=self.USER_PASSWORD
        )
        response = self.client.get('/register', follow=True)
        url, status_code = response.redirect_chain[0]
        self.assertEquals(status_code, 302)
        self.assertEquals(url, 'http://testserver/')


class LoginWebTestCase(TestCase):

    USER_USERNAME = 'jsmith'
    USER_EMAIL = 'jsmith@example.com'
    USER_PASSWORD = 'abc123'

    def setUp(self):
        super(LoginWebTestCase, self).setUp()
        self.client = Client()
        self.user_profile = UserProfile.objects.create_account(
            username=self.USER_USERNAME,
            email=self.USER_EMAIL,
            password=self.USER_PASSWORD
        )

    def testLoginPageRenders(self):
        response = self.client.get('/login')
        self.assertEquals(response.status_code, 200)

    def testUserLogsIn(self):
        self.client.get('/login')
        payload = {
            'username': self.USER_USERNAME,
            'password': self.USER_PASSWORD,
        }
        response = self.client.post('/login', payload, follow=True)
        url, status_code = response.redirect_chain[0]
        self.assertEquals(status_code, 302)
        self.assertEquals(url, 'http://testserver/')

    def testRedirectsAuthenticatedUsersToHome(self):
        self.client.login(
            username=self.USER_USERNAME,
            password=self.USER_PASSWORD
        )
        response = self.client.get('/login', follow=True)
        url, status_code = response.redirect_chain[0]
        self.assertEquals(status_code, 302)
        self.assertEquals(url, 'http://testserver/')


class LogoutWebTestCase(TestCase):

    USER_USERNAME = 'jsmith'
    USER_EMAIL = 'jsmith@example.com'
    USER_PASSWORD = 'abc123'

    def setUp(self):
        super(LogoutWebTestCase, self).setUp()
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

    def testRedirectsAfterLogoutToLogin(self):
        response = self.client.get('/logout', follow=True)
        url, status_code = response.redirect_chain[0]
        self.assertEquals(status_code, 302)
        self.assertEquals(url, 'http://testserver/login')

    def testRedirectsUnauthenticatedUsersToLogin(self):
        self.client.logout()
        response = self.client.get('/logout', follow=True)
        url, status_code = response.redirect_chain[0]
        self.assertEquals(status_code, 302)
        self.assertEquals(url, 'http://testserver/login')


class ProfileWebTestCase(TestCase):

    USER_USERNAME = 'jsmith'
    USER_EMAIL = 'jsmith@example.com'
    USER_PASSWORD = 'abc123'

    def setUp(self):
        super(ProfileWebTestCase, self).setUp()
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

    def testProfilePageRenders(self):
        response = self.client.get('/profile')
        self.assertEquals(response.status_code, 200)

    def testRedirectsUnauthenticatedUsersToLogin(self):
        self.client.logout()
        response = self.client.get('/profile', follow=True)
        url, status_code = response.redirect_chain[0]
        self.assertEquals(status_code, 302)
        self.assertEquals(url, 'http://testserver/login/?next=/profile')
