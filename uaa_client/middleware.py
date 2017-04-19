import logging
import time
from django.contrib.auth import logout

try:
    from django.utils.deprecation import MiddlewareMixin  # pragma: no cover
except ImportError:  # pragma: no cover
    MiddlewareMixin = object  # pragma: no cover

from .authentication import update_access_token_with_refresh_token


logger = logging.getLogger('uaa_client')


def uaa_refresh_exempt(func):
    func.uaa_refresh_exempt = True
    return func


class UaaRefreshMiddleware(MiddlewareMixin):
    def _refresh(self, request):
        username = request.user.username
        if update_access_token_with_refresh_token(request) is None:
            logger.info(
                'Refreshing token for {} failed.'.format(username)
            )
            logout(request)
        else:
            logger.info(
                'Refreshing token for {} succeeded.'.format(username)
            )

    def process_view(self, request, view_func, view_args, view_kwargs):
        should_refresh = (
            request.user.is_authenticated() and
            'uaa_expiry' in request.session and
            time.time() > request.session['uaa_expiry'] and
            not getattr(view_func, 'uaa_refresh_exempt', False)
        )

        if should_refresh:
            self._refresh(request)
