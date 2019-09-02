"""
:Created: 15 August 2015
:Author: Lucas Connors

"""

from django.contrib.auth.models import User
from django.db import IntegrityError, models

from users.exceptions import UserAlreadyExistsException


class UserProfileManager(models.Manager):
    def create_account(
        self, username, email, password, first_name=None, last_name=None
    ):
        # Verify that email is unique
        if User.objects.filter(email=email).exists():
            raise UserAlreadyExistsException(
                f"A user with the email {email} already exists."
            )

        # Create user object
        try:
            user = User.objects.create_user(username, email, password)
        except IntegrityError:
            raise UserAlreadyExistsException(
                "A user with the username {username} already exists.".format(
                    username=username
                )
            )
        if first_name or last_name:
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            user.save()

        # Create user profile object
        user_profile = self.create(user=user)
        return user_profile
