import logging
import time
from django.contrib.auth import logout

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

from .authentication import update_access_token_with_refesh_token


logger = logging.getLogger('uaa_client')


class UaaRefreshMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        should_refresh = (
            request.user.is_authenticated() and
            'uaa_expiry' in request.session and
            time.time() > request.session['uaa_expiry'] and
            not getattr(view_func, 'uaa_refresh_exempt', False)
        )

        if should_refresh:
            username = request.user.username
            if update_access_token_with_refesh_token(request) is None:
                logger.info(
                    'Refreshing token for {} failed.'.format(username)
                )
                logout(request)
            else:
                logger.info(
                    'Refreshing token for {} succeded.'.format(username)
                )
