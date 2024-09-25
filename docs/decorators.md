# Decorators

***uaa_client.decorators.staff_login_required(function=None, redirect_field_name='next', login_url=None)***

Decorator to check that the user accessing the decorated view has their `is_staff` flag set to `True`.

It will first redirect to `login_url` or the default login url if the user is not authenticated. If the user is authenticated but is not staff, then a **`django.core.exceptions.PermissionDenied`** exception will be raised.
