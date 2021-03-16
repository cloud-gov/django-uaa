import logging
import time
from typing import Callable, Iterable, Dict
from django.contrib.auth import logout
from django.http.request import HttpRequest

try:
    from django.utils.deprecation import MiddlewareMixin  # pragma: no cover
except ImportError:  # pragma: no cover
    # We're on Django 1.8 or 1.9.
    MiddlewareMixin = object  # pragma: no cover

from .compat import is_user_authenticated
from .authentication import update_access_token_with_refresh_token

logger = logging.getLogger("uaa_client")


class UaaRefreshMiddleware(MiddlewareMixin):
    """
    This middleware checks to see if a logged-in user's UAA access token
    has expired; if it has, it will attempt to use the user's refresh token
    to obtain a new access token.

    If the refresh fails, then the user is logged out.

    Note that this middleware is very important from a security
    standpoint: short-lived access tokens combined with the token refresh
    process ensures that unauthorized users are logged out of the system
    as soon as possible.
    """

    def _refresh(self, request: HttpRequest) -> None:
        username = request.user.username
        if update_access_token_with_refresh_token(request) is None:
            logger.info("Refreshing token for {} failed.".format(username))
            logout(request)
        else:
            logger.info("Refreshing token for {} succeeded.".format(username))

    def process_view(
        self,
        request: HttpRequest,
        view_func: Callable,
        view_args: Iterable,
        view_kwargs: Dict,
    ) -> None:
        should_refresh = (
            is_user_authenticated(request.user)
            and "uaa_expiry" in request.session
            and time.time() > request.session["uaa_expiry"]
            and not getattr(view_func, "uaa_refresh_exempt", False)
        )

        if should_refresh:
            self._refresh(request)


def uaa_refresh_exempt(func: Callable) -> Callable:
    """
    View decorator that exempts a view from the UAA refresh middleware
    logic.
    """

    setattr(func, "uaa_refresh_exempt", True)
    return func
