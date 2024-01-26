"""example URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

import django
from django.shortcuts import render, redirect
from django.conf.urls import include
from django.urls import re_path
from django.contrib import admin, auth

from uaa_client.decorators import staff_login_required

admin.site.login = staff_login_required(admin.site.login)


def index(request):
    return render(request, "index.html")


def logout(request):
    auth.logout(request)
    return redirect("/")


_kwargs = {}

if django.get_version().startswith("1.8."):
    _kwargs["namespace"] = "uaa_client"

urlpatterns = [
    re_path(r"^$", index),
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^auth/", include("uaa_client.urls", **_kwargs)),
    re_path(r"^logout/", logout, name="logout"),
]
