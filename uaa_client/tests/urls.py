import django

from django.conf.urls import include
from django.urls import re_path

_kwargs = {}

if django.get_version().startswith("1.8."):
    _kwargs["namespace"] = "uaa_client"

urlpatterns = [re_path(r"^auth/", include("uaa_client.urls", **_kwargs))]
