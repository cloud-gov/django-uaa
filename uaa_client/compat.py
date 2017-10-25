try:
    from django.core.urlresolvers import reverse  # NOQA
except ImportError:
    # Django 2.0+
    from django.urls import reverse  # NOQA


def is_user_authenticated(user):
    if callable(user.is_authenticated):
        return user.is_authenticated()

    # Django 2.0+
    return user.is_authenticated
