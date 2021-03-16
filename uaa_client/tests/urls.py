import django
from django.conf.urls import include, url

_kwargs = {}

if django.get_version().startswith("1.8."):
    _kwargs["namespace"] = "uaa_client"

urlpatterns = [url(r"^auth/", include("uaa_client.urls", **_kwargs))]
