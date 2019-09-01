"""
:Created: 15 August 2015
:Author: Lucas Connors

"""

from django.contrib import admin

from users.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):

    list_display = ("id", "username", "email", "full_name")

    def username(self, userprofile):
        return userprofile.user.username

    def email(self, userprofile):
        return userprofile.user.email


admin.site.register(UserProfile, UserProfileAdmin)
