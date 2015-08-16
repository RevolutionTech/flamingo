"""
:Created: 15 August 2015
:Author: Lucas Connors

"""

from django.contrib import admin

from users.models import UserProfile


admin.site.register(UserProfile)
