"""
:Created: 16 August 2015
:Author: Lucas Connors

"""

import functools

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect


def redirect_authenticated(func):
    """ If the user is already authenticated, redirect to home """

    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('home'))
        return func(request, *args, **kwargs)

    return wrapper
