"""
:Created: 16 August 2015
:Author: Lucas Connors

"""

from django import forms
from django.contrib.auth.models import User
from django.core.validators import validate_email


class RegisterForm(forms.Form):

    username = forms.CharField(max_length=75)
    email = forms.EmailField()
    password = forms.CharField()
    password_confirm = forms.CharField()
    first_name = forms.CharField(required=False, max_length=30)
    last_name = forms.CharField(required=False, max_length=30)

    def clean_username(self):
        """ Verify that the username is not already taken """

        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "Sorry! An account with this username already exists."
            )
        return username

    def clean_email(self):
        """ Verify that the email is not already registered """

        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "An account with this email address already exists."
            )
        return email

    def clean(self):
        """
        Verify that user does not already exist and
        that password and password_confirm fields match
        """

        cleaned_data = super().clean()

        if not self.errors:
            password = cleaned_data.get("password")
            password_confirm = cleaned_data.get("password_confirm")

            if password != password_confirm:
                raise forms.ValidationError(
                    "Password and Password Confirm fields do not match."
                )

        return cleaned_data


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
        except forms.ValidationError:
            username = email_or_username
        else:
            email = email_or_username

        if email:
            try:
                return User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError(cls.FAILED_AUTH_WARNING)
        else:  # username
            try:
                return User.objects.get(username=username)
            except User.DoesNotExist:
                raise forms.ValidationError(cls.FAILED_AUTH_WARNING)

    def clean(self):
        """ Verify that user with given credentials exists """

        cleaned_data = super().clean()

        if not self.errors:
            email_or_username = cleaned_data.get("username")
            password = cleaned_data.get("password")
            user = self.user_from_email_or_username(email_or_username)
            if user and user.check_password(password):
                cleaned_data["email"] = user.email
                cleaned_data["username"] = user.username
            else:
                raise forms.ValidationError(self.FAILED_AUTH_WARNING)

        return cleaned_data
