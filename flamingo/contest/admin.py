"""
:Created: 16 August 2015
:Author: Lucas Connors

"""

from django.contrib import admin

from contest.models import Sponsor, Contest


admin.site.register(Sponsor)
admin.site.register(Contest)
