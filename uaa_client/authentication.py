import logging
import requests
import jwt
from django.core.exceptions import MultipleObjectsReturned
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.conf import settings

logger = logging.getLogger('uaa_client')


def get_auth_url(request):
    if settings.DEBUG and settings.UAA_AUTH_URL == 'fake:':
        return request.build_absolute_uri(reverse('uaa_client:fake_auth'))
    return settings.UAA_AUTH_URL


def get_token_url(request):
    if settings.DEBUG and settings.UAA_TOKEN_URL == 'fake:':
        return request.build_absolute_uri(reverse('uaa_client:fake_token'))
    return settings.UAA_TOKEN_URL


def exchange_code_for_access_token(request, code):
    redirect_uri = request.build_absolute_uri(reverse('uaa_client:callback'))

    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'response_type': 'token',
        'client_id': settings.UAA_CLIENT_ID,
        'client_secret': settings.UAA_CLIENT_SECRET
    }

    token_url = get_token_url(request)
    token_req = requests.post(token_url, data=payload)
    if token_req.status_code != 200:
        logger.warning('POST %s returned %s '
                       'w/ content %s' % (
                           token_url,
                           token_req.status_code,
                           repr(token_req.content)
                       ))
        return None

    response = token_req.json()
    request.session.set_expiry(response['expires_in'])

    return response['access_token']


class UaaBackend(ModelBackend):
    '''
    Custom auth backend for Cloud Foundry / cloud.gov User Account and
    Authentication (UAA) servers.

    This inherits from :class:`django.contrib.auth.backends.ModelBackend`
    so that the superclass can provide all authorization methods.
    '''

    @staticmethod
    def get_user_by_email(email):
        '''
        Return a :class:`django.contrib.auth.models.User` with the given
        email address. If no user can be found, return ``None``.

        The default implementation attempts to find an existing user with
        the given case-insensitive email address. If no such user exists,
        ``None`` is returned.

        Subclasses may override this method to account for different kinds
        of security policies for logins.
        '''

        try:
            return User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            logger.info(
                'User with email {} does not exist'.format(email)
            )
            return None
        except MultipleObjectsReturned:
            logger.warning(
                'Multiple users with email {} exist'.format(email)
            )
            return None

    def authenticate(self, uaa_oauth2_code=None, request=None, **kwargs):
        if uaa_oauth2_code is None or request is None:
            return None

        access_token = exchange_code_for_access_token(request, uaa_oauth2_code)
        if access_token is None:
            return None

        user_info = jwt.decode(access_token, verify=False)

        return self.get_user_by_email(user_info['email'])
