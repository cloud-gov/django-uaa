import functools
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib import auth
from django.http import HttpResponseNotFound

from .authentication import UaaBackend


# To determine whether we're running tests, we're going to remember the
# earliest value of settings.DEBUG at the time that our app was initialized.
# For more details on why this is important, see:
#
# https://github.com/18F/cg-django-uaa/issues/18
earliest_debug_setting = settings.DEBUG


def validate_configuration(use_earliest_debug_setting=True):
    for setting in [
        "UAA_CLIENT_ID",
        "UAA_CLIENT_SECRET",
        "UAA_AUTH_URL",
        "UAA_TOKEN_URL",
    ]:
        val = getattr(settings, setting, None)
        if not (val and isinstance(val, str)):
            raise ImproperlyConfigured(
                "settings.{} must be defined as a " "non-empty string".format(setting)
            )

    if (settings.UAA_AUTH_URL == "fake:" and settings.UAA_TOKEN_URL != "fake:") or (
        settings.UAA_TOKEN_URL == "fake:" and settings.UAA_AUTH_URL != "fake:"
    ):
        raise ImproperlyConfigured(
            "If one of settings.UAA_AUTH_URL or "
            'settings.UAA_TOKEN_URL is "fake:", the other '
            'must also be set to "fake:"'
        )

    debug = settings.DEBUG
    if use_earliest_debug_setting:
        debug = earliest_debug_setting

    if not debug:
        if not (
            settings.UAA_AUTH_URL.startswith("https://")
            and settings.UAA_TOKEN_URL.startswith("https://")
        ):
            raise ImproperlyConfigured(
                "In production, UAA_AUTH_URL and UAA_TOKEN_URL must " "both use https."
            )

    uaa_backend_found = False
    for backend in auth.get_backends():
        if isinstance(backend, UaaBackend):
            uaa_backend_found = True

    if not uaa_backend_found:
        raise ImproperlyConfigured(
            "settings.AUTHENTICATION_BACKENDS must contain an instance "
            "of {}".format(UaaBackend.__name__)
        )


def require_debug(func):
    """
    Decorator that wraps a Django view so it's only enabled when
    settings.DEBUG is True.  If settings.DEBUG is False, the view will
    always return a 404.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not settings.DEBUG:
            return HttpResponseNotFound()
        return func(*args, **kwargs)

    return wrapper
