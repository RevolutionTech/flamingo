"""
:Created: 29 August 2015
:Author: Lucas Connors

"""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.utils import timezone

from contest.forms import UploadPhotoForm
from contest.models import Sponsor, Contest, Entry
from photo.models import Photo
from users.models import UserProfile


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


@login_required
def contest_upload_photo_view(request, slug, **kwargs):
    contest = get_object_or_404(Contest, slug=slug)

    # Validate image
    form = UploadPhotoForm(request.POST, request.FILES)
    if not form.is_valid():
        return HttpResponseBadRequest("Image is missing or invalid.")
    cleaned_data = form.cleaned_data

    # Create photo and entry instances
    image = cleaned_data['image']
    photo = Photo.objects.create(
        user_profile=UserProfile.objects.get(user=request.user),
        title=image.name,
        img=image,
    )
    Entry.objects.create(
        contest=contest,
        photo=photo
    )

    # Reply to upload with 205
    return HttpResponse(status=205)
