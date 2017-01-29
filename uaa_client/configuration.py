from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def validate_configuration():
    for setting in ['UAA_CLIENT_ID', 'UAA_CLIENT_SECRET',
                    'UAA_AUTH_URL', 'UAA_TOKEN_URL']:
        val = getattr(settings, setting, None)
        if not (val and isinstance(val, str)):
            raise ImproperlyConfigured(
                'settings.{} must be defined as a '
                'non-empty string'.format(setting)
            )

    if ((settings.UAA_AUTH_URL == 'fake:' and
            settings.UAA_TOKEN_URL != 'fake:') or
            (settings.UAA_TOKEN_URL == 'fake:' and
                settings.UAA_AUTH_URL != 'fake:')):
        raise ImproperlyConfigured(
            'If one of settings.UAA_AUTH_URL or '
            'settings.UAA_TOKEN_URL is "fake:", the other '
            'must also be set to "fake:"'
        )

    if not settings.DEBUG:
        if not (settings.UAA_AUTH_URL.startswith('https://') and
                settings.UAA_TOKEN_URL.startswith('https://')):
            raise ImproperlyConfigured(
                'In production, UAA_AUTH_URL and UAA_TOKEN_URL must '
                'both use https.'
            )
