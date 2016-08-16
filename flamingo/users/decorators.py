"""
:Created: 16 August 2015
:Author: Lucas Connors

"""

import functools

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


def redirect_authenticated(func):
    """ If the user is already authenticated, redirect to home """

    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))
        return func(request, *args, **kwargs)

    return wrapper


def authenticated_or_401(func):
    """ If the user is not authenticated, return a 401 HTTP status code """

    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse(
                "You must be logged in to perform this action.",
                status=401
            )
        return func(request, *args, **kwargs)

    return wrapper
