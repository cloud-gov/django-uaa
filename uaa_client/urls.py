from django.conf.urls import url

from . import views, fake_uaa_provider
from .configuration import validate_configuration, require_debug


app_name = "uaa_client"

urlpatterns = [
    url(r"^callback$", views.oauth2_callback, name="callback"),
    url(r"^login$", views.login, name="login"),
    url(
        r"^fake/oauth/authorize$",
        require_debug(fake_uaa_provider.authorize),
        name="fake_auth",
    ),
    url(
        r"^fake/oauth/token$",
        require_debug(fake_uaa_provider.access_token),
        name="fake_token",
    ),
]

validate_configuration()
