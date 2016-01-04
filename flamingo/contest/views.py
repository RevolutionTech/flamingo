"""
:Created: 29 August 2015
:Author: Lucas Connors

"""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, \
    HttpResponseNotFound
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
        context['contests_submission_open'] = Contest.objects.filter(
            submission_open__lte=now,
            submission_close__gt=now
        )
        context['contests_voting_open'] = Contest.objects.filter(
            submission_close__lte=now,
            end__gt=now
        )
        context['contests_ended'] = Contest.objects.filter(end__lte=now)
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
        user = self.request.user
        contest = Contest.objects.get(slug=slug)

        context['contest'] = contest
        context['submissions_open'] = contest.submission_close > timezone.now()
        context['voting_open'] = contest.end > timezone.now()
        context['entries'] = map(
            lambda entry: {
                'id': entry.id,
                'photo': entry.photo,
                'vote_count': entry.vote_count(),
                'has_upvoted': entry.has_upvoted(user),
                'has_downvoted': entry.has_downvoted(user),
            },
            Entry.objects.filter(contest=contest).order_by('?')
        )
        return context


@login_required
def contest_upload_photo(request, slug, **kwargs):
    contest = get_object_or_404(Contest, slug=slug)

    # Check that submission date has not passed
    if timezone.now() >= contest.submission_close:
        return HttpResponseBadRequest(
            "Photo submission period for contest has ended."
        )

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


@login_required
def contest_vote_entry(request, contest_slug, entry_id, vote_type, **kwargs):
    contest = get_object_or_404(Contest, slug=contest_slug)
    entry = get_object_or_404(Entry, id=entry_id)

    # Verify that the entry belongs to the contest
    if entry.contest != contest:
        return HttpResponseNotFound("")

    # Check that contest has not already ended
    if timezone.now() >= contest.end:
        return HttpResponseBadRequest("Voting period for contest has ended.")

    vote_count = entry.vote(user=request.user, vote_type=vote_type)

    # Reply to vote with vote count
    return JsonResponse({'vote_count': vote_count})
