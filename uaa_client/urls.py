from django.urls import re_path

from . import views, fake_uaa_provider
from .configuration import validate_configuration, require_debug


app_name = "uaa_client"

urlpatterns = [
    re_path(r"^callback$", views.oauth2_callback, name="callback"),
    re_path(r"^login$", views.login, name="login"),
    re_path(
        r"^fake/oauth/authorize$",
        require_debug(fake_uaa_provider.authorize),
        name="fake_auth",
    ),
    re_path(
        r"^fake/oauth/token$",
        require_debug(fake_uaa_provider.access_token),
        name="fake_token",
    ),
]

validate_configuration()
