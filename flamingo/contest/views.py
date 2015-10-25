"""
:Created: 29 August 2015
:Author: Lucas Connors

"""

from django.views.generic import TemplateView
from django.utils import timezone

from contest.models import Sponsor, Contest, Entry


class HomeView(TemplateView):

    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        now = timezone.now()
        context['contests'] = Contest.objects.filter(
            submission_open__lte=now,
            submission_close__gt=now
        )
        return context


class SponsorDetailsView(TemplateView):

    template_name = 'sponsor_details.html'

    def get_context_data(self, slug, **kwargs):
        context = super(SponsorDetailsView, self).get_context_data(**kwargs)
        context['sponsor'] = Sponsor.objects.get(slug=slug)
        return context


class ContestDetailsView(TemplateView):

    template_name = 'contest_details.html'

    def get_context_data(self, slug, **kwargs):
        context = super(ContestDetailsView, self).get_context_data(**kwargs)
        contest = Contest.objects.get(slug=slug)
        context['contest'] = contest
        context['entries'] = Entry.objects.filter(contest=contest)
        return context
