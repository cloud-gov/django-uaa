Quick start guide
=================

Prerequisites
~~~~~~~~~~~~~

You will need Python 3.5 or above, and Django 1.8 or above.

Installation
~~~~~~~~~~~~

To install cg-django-uaa, run::

    pip install cg-django-uaa

Required settings
~~~~~~~~~~~~~~~~~

Begin by adding the following setting to your Django settings file:

``UAA_CLIENT_ID``
    This is your app's client ID for cloud.gov UAA.

``UAA_CLIENT_SECRET``
    This is your app's client secret for cloud.gov UAA.

``UAA_AUTH_URL``
    This is the URL for the authorize endpoint for cloud.gov, e.g.
    ``https://login.fr.cloud.gov/oauth/authorize``.

``UAA_TOKEN_URL``
    This is the URL for the token endpoint for cloud.gov, e.g.
    ``https://uaa.fr.cloud.gov/oauth/token``. Note that it may
    be at an entirely different domain from the authorize endpoint.

Also make sure you add ``'uaa_client.authentication.UaaBackend'`` to
your ``AUTHENTICATION_BACKENDS`` setting.

.. important::

    The default authentication backend will only allow users with existing
    models in your database to log in, which means that you'll probably
    need to manually create users through Django's admin UI or via
    ``manage.py createsuperuser``.

    To override this default behavior, you may subclass
    :class:`uaa_client.authentication.UaaBackend`.

You will likely want to set ``LOGIN_URL`` to ``'uaa_client:login'``, so
that any views which require login will automatically be redirected
to cloud.gov-based login.

You'll also need to have ``django.contrib.auth`` and ``uaa_client`` in your
``INSTALLED_APPS`` setting.

Finally, you will also need to add
``uaa_client.middleware.UaaRefreshMiddleware`` to your ``MIDDLEWARE``
setting (or ``MIDDLEWARE_CLASSES`` if you're on Django 1.8 or 1.9). It needs
to be placed after Django's session and authentication
middleware, e.g.:

.. code-block:: python

   MIDDLEWARE = [
       # ...
       'django.contrib.sessions.middleware.SessionMiddleware',
       'django.contrib.auth.middleware.AuthenticationMiddleware',
       'uaa_client.middleware.UaaRefreshMiddleware',
       # ...
   ]

Setting up URLs
~~~~~~~~~~~~~~~

You will want to add the following to your Django project's URLconf.

.. code-block:: python

   from django.conf.urls import include, url

   urlpatterns = [
       # Other URL patterns ...
       url(r'^auth/', include('uaa_client.urls')),
       # More URL patterns ...
   ]

If you are using Django 1.8, you will need to additionally pass a
``namespace="uaa_client"`` keyword argument to ``include()``.

Required templates
~~~~~~~~~~~~~~~~~~

You will also need to create at least one template to use cg-django-uaa.

All of these are rendered using a ``RequestContext`` and so will also
receive any additional variables provided by `context processors
<https://docs.djangoproject.com/en/stable/ref/templates/api/>`_.

**uaa_client/login_error.html**

Used to show that the user has encountered some sort of error
when trying to authenticate with cloud.gov, or when trying to associate
a cloud.gov user with a Django user.  The context contains
a single variable, ``error_code``, which can have a variety of
string values, including:

``'authenticate_failed'``
    This means that the underlying call to
    :func:`django.contrib.auth.authenticate` returned ``None`` instead of
    a user. The actual reasons for the failure depend on the 
    :class:`uaa_client.authentication.UaaBackend` your project is
    configured to use; it could mean, for instance, that the OAuth2
    code passed back from the cloud.gov's authorize endpoint was invalid,
    or there exists no user model with an email address corresponding
    to the user who just logged in via cloud.gov.

    You may learn more about why authentication failed by enabling
    logging output for the ``uaa_client`` logger at the ``INFO`` level. While
    configuring logging is outside of the scope of this guide, you may
    refer to the `example project's settings
    <https://github.com/18F/cg-django-uaa/blob/master/example/example/settings.py>`_
    for an example.

The other error codes generally refer to mishaps in the OAuth2 protocol
and can be discovered by examining the ``uaa_client.views`` module.

.. _fakeauth:

Using the fake cloud.gov server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is possible to use a fake UAA provider for development purposes.
This allows developers to simply enter any email address and
automatically be logged-in as that user.

.. image:: /_static/fake-cloud-gov.png

To enable this functionality, set the ``UAA_AUTH_URL`` and
``UAA_TOKEN_URL`` settings to ``'fake:'``.

As this feature would clearly be a security hazard if used in
production, it is *only* available when ``DEBUG`` is ``True``.

Note also that the fake server won't work properly if the web
server hosting your Django project can't handle more than one
request at a time. This generally shouldn't be a problem, since
``manage.py runserver`` doesn't have this limitation. If you're using
gunicorn to serve your app in ``DEBUG`` mode, though, you may want to
make sure that your ``WEB_CONCURRENCY`` environment variable is
set to a value greater than 1.
