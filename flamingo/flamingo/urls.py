"""
:Created: 16 August 2015
:Author: Lucas Connors

"""

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.static import serve

from contest.views import HomeView
from users.decorators import redirect_authenticated
from users.views import RegisterView, LoginView, logout, ProfileView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/?$', redirect_authenticated(RegisterView.as_view()), name='register'),
    url(r'^login/?$', redirect_authenticated(LoginView.as_view()), name='login'),
    url(r'^logout/?$', logout, name='logout'),
    url(r'^profile/?$', login_required(ProfileView.as_view()), name='profile'),
    url(r'^/?$', login_required(HomeView.as_view()), name='home'),
]

# Add media folder to urls when DEBUG = True
if settings.DEBUG:
    urlpatterns.append(
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
    )
