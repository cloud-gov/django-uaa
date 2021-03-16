import logging

from django.contrib.auth import REDIRECT_FIELD_NAME, decorators
from django.core.exceptions import PermissionDenied

from .compat import is_user_authenticated


logger = logging.getLogger("uaa_client")


def staff_login_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None
):
    """
    Decorator to check that the user accessing the decorated view has their
    ``is_staff`` flag set to ``True``.

    It will first redirect to ``login_url`` or the default login url if the
    user is not authenticated. If the user is authenticated but is not
    staff, then a :class:`django.core.exceptions.PermissionDenied` exception
    will be raised.
    """

    # This is based off code from the Django project:
    # License: https://github.com/django/django/blob/c1aec0feda73ede09503192a66f973598aef901d/LICENSE  # NOQA
    # Code reference: https://github.com/django/django/blob/c1aec0feda73ede09503192a66f973598aef901d/django/contrib/auth/decorators.py#L40  # NOQA
    def check_if_staff(user):
        if not is_user_authenticated(user):
            # Returning False will cause the user_passes_test decorator
            # to redirect the client to the login flow.
            logger.info("Unauthenticated user has attempted to access " "is_staff view")
            return False

        if user.is_staff:
            # The user is staff, all is good!
            logger.info(
                "User with id {} ({}) has passed "
                "is_staff check".format(user.id, user.email)
            )
            return True

        # Otherwise, the user is authenticated but isn't staff, so
        # they do not have the correct permissions and should be directed
        # to the 403 page.
        logger.info(
            "User with id {} ({}) is "
            "authenticated but has not passed is_staff "
            "check".format(user.id, user.email)
        )
        raise PermissionDenied

    actual_decorator = decorators.user_passes_test(
        check_if_staff, login_url=login_url, redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
