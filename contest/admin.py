"""
:Created: 16 August 2015
:Author: Lucas Connors

"""

from django.contrib import admin

from contest.models import Contest, Entry, Sponsor


class SponsorAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class ContestAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(Contest, ContestAdmin)
admin.site.register(Entry)
