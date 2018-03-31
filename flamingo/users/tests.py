"""
:Created: 15 August 2015
:Author: Lucas Connors

"""

from django.contrib.auth.models import User

from flamingo.tests import FlamingoTestCase, FlamingoTransactionTestCase
from users.exceptions import UserAlreadyExistsException
from users.forms import RegisterForm, LoginForm
from users.models import UserProfile


class UserTestCase(FlamingoTransactionTestCase):

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
            str(created_user_profile),
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


class UserAdminWebTestCase(FlamingoTestCase):

    def get200s(self):
        return [
            '/admin/users/',
            '/admin/users/userprofile/',
            '/admin/users/userprofile/add/',
            '/admin/users/userprofile/{userprofile_id}/change/'.format(
                userprofile_id=self.user_profile.id
            ),
        ]


class RegisterFormTestCase(FlamingoTestCase):

    def testUsernameAlreadyTaken(self):
        form_data = {
            'username': self.USER_USERNAME,
            'email': self.CREATED_USER_EMAIL,
            'password': self.USER_PASSWORD,
            'password_confirm': self.USER_PASSWORD,
        }
        form = RegisterForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def testEmailAlreadyRegistered(self):
        form_data = {
            'username': self.CREATED_USER_USERNAME,
            'email': self.USER_EMAIL,
            'password': self.USER_PASSWORD,
            'password_confirm': self.USER_PASSWORD,
        }
        form = RegisterForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def testPasswordsDoNotMatch(self):
        form_data = {
            'username': self.CREATED_USER_USERNAME,
            'email': self.CREATED_USER_EMAIL,
            'password': self.USER_PASSWORD,
            'password_confirm': "oops123",
        }
        form = RegisterForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        self.assertEquals(len(form.errors['__all__']), 1)
        (error,) = form.errors['__all__']
        self.assertIn('Password', error)
        self.assertIn('not match', error)


class RegisterWebTestCase(FlamingoTestCase):

    def testRegisterPageRenders(self):
        self.client.logout()
        self.assertResponseRenders('/register')

    def testUserRegisters(self):
        self.client.logout()
        UserProfile.objects.all().delete()
        self.assertResponseRenders('/register')
        payload = {
            'username': self.CREATED_USER_USERNAME,
            'email': self.CREATED_USER_EMAIL,
            'password': self.USER_PASSWORD,
            'password_confirm': self.USER_PASSWORD,
            'first_name': self.CREATED_USER_FIRST_NAME,
            'last_name': self.CREATED_USER_LAST_NAME,
        }
        self.assertResponseRedirects('/register', '/', method='POST', data=payload)
        self.assertEquals(UserProfile.objects.all().count(), 1)

    def testRedirectsAuthenticatedUsersToHome(self):
        self.assertResponseRedirects('/register', '/')


class LoginFormTestCase(FlamingoTestCase):

    UNCREATED_USER_USERNAME = 'UncreatedUser'
    UNCREATED_USER_EMAIL = 'uncreated@example.com'

    def testUsernameDoesNotExist(self):
        form_data = {
            'username': self.UNCREATED_USER_USERNAME,
            'password': self.USER_PASSWORD,
        }
        form = LoginForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        self.assertEquals(len(form.errors['__all__']), 1)
        (error,) = form.errors['__all__']
        self.assertEquals(error, LoginForm.FAILED_AUTH_WARNING)

    def testEmailDoesNotExist(self):
        form_data = {
            'username': self.UNCREATED_USER_EMAIL,
            'password': self.USER_PASSWORD,
        }
        form = LoginForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        self.assertEquals(len(form.errors['__all__']), 1)
        (error,) = form.errors['__all__']
        self.assertEquals(error, LoginForm.FAILED_AUTH_WARNING)

    def testPasswordIncorrect(self):
        form_data = {
            'username': self.USER_USERNAME,
            'password': 'oops123',
        }
        form = LoginForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        self.assertEquals(len(form.errors['__all__']), 1)
        (error,) = form.errors['__all__']
        self.assertEquals(error, LoginForm.FAILED_AUTH_WARNING)


class LoginWebTestCase(FlamingoTestCase):

    def testLoginPageRenders(self):
        self.client.logout()
        self.assertResponseRenders('/login')

    def testUserLogsIn(self):
        self.client.logout()
        self.assertResponseRenders('/login')
        payload = {
            'username': self.USER_USERNAME,
            'password': self.USER_PASSWORD,
        }
        self.assertResponseRedirects('/login', '/', method='POST', data=payload)

    def testUserLogsInWithEmail(self):
        self.client.logout()
        self.assertResponseRenders('/login')
        payload = {
            'username': self.USER_EMAIL,
            'password': self.USER_PASSWORD,
        }
        self.assertResponseRedirects('/login', '/', method='POST', data=payload)

    def testRedirectsAuthenticatedUsersToHome(self):
        self.assertResponseRedirects('/login', '/')


class LogoutWebTestCase(FlamingoTestCase):

    def testRedirectsAfterLogoutToLogin(self):
        self.assertResponseRedirects('/logout', '/login')

    def testRedirectsUnauthenticatedUsersToLogin(self):
        self.client.logout()
        self.assertResponseRedirects('/logout', '/login')


class ProfileWebTestCase(FlamingoTestCase):

    def get200s(self):
        return [
            '/profile',
        ]

    def testRedirectsUnauthenticatedUsersToLogin(self):
        self.client.logout()
        self.assertResponseRedirects('/profile', '/login/')
