"""
:Created: 16 August 2015
:Author: Lucas Connors

"""

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from users.forms import LoginForm, RegisterForm
from users.models import UserProfile


class RegisterView(FormView):

    template_name = "register.html"
    form_class = RegisterForm

    def dispatch(self, request):
        self.success_url = request.GET.get("next", reverse("home"))
        return super().dispatch(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["redirect_url"] = self.success_url
        return context

    def form_valid(self, form):
        d = form.cleaned_data
        username, password = d["username"], d["password"]
        UserProfile.objects.create_account(
            username=username,
            email=d["email"],
            password=password,
            first_name=d["first_name"],
            last_name=d["last_name"],
        )
        user = authenticate(username=username, password=password)
        if user:
            auth_login(self.request, user)
            return super().form_valid(form)


class LoginView(FormView):

    template_name = "login.html"
    form_class = LoginForm

    def dispatch(self, request):
        self.success_url = request.GET.get("next", reverse("home"))
        return super().dispatch(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["redirect_url"] = self.success_url
        return context

    def form_valid(self, form):
        d = form.cleaned_data
        username, password = d["username"], d["password"]
        user = authenticate(username=username, password=password)
        if user:
            auth_login(self.request, user)
            return super().form_valid(form)


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse("login"))


class ProfileView(TemplateView):

    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_profile"] = self.request.user.userprofile
        return context
