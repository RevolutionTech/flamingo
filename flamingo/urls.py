"""
:Created: 16 August 2015
:Author: Lucas Connors

"""

from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.static import serve

from contest.models import Vote
from contest.views import (
    ContestDetailsView,
    HomeView,
    SponsorDetailsView,
    contest_upload_photo,
    contest_vote_entry,
)
from users.decorators import redirect_authenticated
from users.views import LoginView, ProfileView, RegisterView, logout

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(
        r"^register/?$", redirect_authenticated(RegisterView.as_view()), name="register"
    ),
    url(r"^login/?$", redirect_authenticated(LoginView.as_view()), name="login"),
    url(r"^logout/?$", logout, name="logout"),
    url(
        r"^sponsor/details/(?P<slug>[\w_-]+)/?$",
        SponsorDetailsView.as_view(),
        name="sponsor_details",
    ),
    url(
        r"^contest/details/(?P<contest_slug>[\w_-]+)/entry/(?P<entry_id>\d+)/upvote/?$",
        contest_vote_entry,
        {"vote_type": Vote.UPVOTE},
        name="contest_upvote_entry",
    ),
    url(
        r"^contest/details/(?P<contest_slug>[\w_-]+)/entry/(?P<entry_id>\d+)/downvote/?$",
        contest_vote_entry,
        {"vote_type": Vote.DOWNVOTE},
        name="contest_downvote_entry",
    ),
    url(
        r"^contest/details/(?P<slug>[\w_-]+)/?$",
        ContestDetailsView.as_view(),
        name="contest_details",
    ),
    url(
        r"^contest/upload/(?P<slug>[\w_-]+)/?$",
        contest_upload_photo,
        name="contest_upload_photo",
    ),
    url(r"^profile/?$", login_required(ProfileView.as_view()), name="profile"),
    url(r"^$", HomeView.as_view(), name="home"),
]

# Add media folder to urls when DEBUG = True
if settings.DEBUG:
    urlpatterns.append(
        url(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT})
    )
