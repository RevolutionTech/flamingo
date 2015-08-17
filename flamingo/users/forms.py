"""
:Created: 16 August 2015
:Author: Lucas Connors

"""

from django import forms
from django.contrib.auth.models import User
from django.core.validators import validate_email


class LoginForm(forms.Form):

    FAILED_AUTH_WARNING = "The email and password do not match our records."

    username = forms.CharField(max_length=75)
    password = forms.CharField()

    @classmethod
    def user_from_email_or_username(cls, email_or_username):
        """ Get user from email/username """

        email = username = None
        try:
            validate_email(email_or_username)
            email = email_or_username
        except forms.ValidationError:
            username = email_or_username

        if email:
            try:
                return User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError(cls.FAILED_AUTH_WARNING)

        elif username:
            try:
                return User.objects.get(username=username)
            except User.DoesNotExist:
                raise forms.ValidationError(cls.FAILED_AUTH_WARNING)

        else:
            raise forms.ValidationError(cls.FAILED_AUTH_WARNING)

    def clean(self):
        """ Verify that user with given credentials exists """

        cleaned_data = super(LoginForm, self).clean()

        if not self.errors:
            email_or_username = cleaned_data.get('username')
            password = cleaned_data.get('password')
            user = self.user_from_email_or_username(email_or_username)
            if user and user.check_password(password):
                cleaned_data['email'] = user.email
                cleaned_data['username'] = user.username
            else:
                raise forms.ValidationError(self.FAILED_AUTH_WARNING)

        return cleaned_data
