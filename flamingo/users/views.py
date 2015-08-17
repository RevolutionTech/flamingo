"""
:Created: 16 August 2015
:Author: Lucas Connors

"""

from django.contrib.auth import authenticate, login as auth_login, \
    logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from users.forms import LoginForm


class LoginView(FormView):

    template_name = 'login.html'
    form_class = LoginForm

    def dispatch(self, request):
        self.success_url = request.GET.get('next', reverse('home'))
        return super(LoginView, self).dispatch(request)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['redirect_url'] = self.success_url
        return context

    def form_valid(self, form):
        d = form.cleaned_data
        username, password = d['username'], d['password']
        user = authenticate(username=username, password=password)
        if user:
            auth_login(self.request, user)
            return super(LoginView, self).form_valid(form)


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('login'))


@login_required
def home(request):
    return HttpResponseRedirect(reverse('profile'))


class ProfileView(TemplateView):

    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['user_profile'] = self.request.user.userprofile
        return context
