try:
    from django.core.urlresolvers import reverse  # NOQA
except ImportError:
    # Django 2.0+
    from django.urls import reverse  # NOQA
