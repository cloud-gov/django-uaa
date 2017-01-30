.. cg-django-uaa documentation master file, created by
   sphinx-quickstart on Mon Jan 30 10:35:02 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to cg-django-uaa's documentation!
=========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

This is a cloud.gov UAA authentication backend for Django. It also
includes a handy "fake cloud.gov" that makes it easy to log in
as any user during development.

.. warning:: This package is in a very early stage of development
   and its settings and/or API will likely change in the near future.
   Use it at your own risk!

   For example, at present, the backend only allows users to log in who
   have existing Django ``User`` models associated with their cloud.gov
   email addresses in the database.

Quick start guide
=================

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

You will likely want to set ``LOGIN_URL`` to ``'uaa_client:login'``, so
that any views which require login will automatically be redirected
to cloud.gov-based login.

You'll also need to have ``django.contrib.auth`` in your
``INSTALLED_APPS`` setting.

.. warning:: You should **not** add ``uaa_client`` to your
   ``INSTALLED_APPS`` setting if you're following this document,
   as it does not make use of any custom models or other fancy features.


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

All of these are rendered using a ``RequestContext`` and so will also
receive any additional variables provided by `context processors
<https://docs.djangoproject.com/en/stable/ref/templates/api/>`_.

**uaa_client/oauth2_error.html**

Used to show that the user has encountered some sort of OAuth2 error
when trying to authenticate with cloud.gov.  The context contains
a single variable, ``error_code``, which can have a variety of
string values, including:

``'invalid_code_or_nonexistent_user'``
    Either the OAuth2 code passed back from the cloud.gov's authorize
    endpoint was invalid, or there exists no ``User`` model with an
    email address corresponding to the user who just logged in via
    cloud.gov.

The meaning of other error codes can be discovered by examining the
``uaa_client.views`` module.

Using the fake cloud.gov server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the ``DEBUG`` setting is ``True``, it is possible to use a fake
UAA provider for development purposes. This allows developers to
simply enter any email address and automatically be logged-in as
that user.

.. image:: https://cloud.githubusercontent.com/assets/124687/16729463/9cd1b676-473a-11e6-98f1-588308c0a213.png

Enabling this functionality requires the following setup.

Firstly, the ``UAA_AUTH_URL`` and ``UAA_TOKEN_URL`` settings
must both be set to ``'fake:'``.

You'll also need to have ``uaa_client.fake_uaa_provider`` in your
``INSTALLED_APPS`` setting.

Finally, you will want to add the fake provider's URLconf to your
project.

.. code-block:: python

   from django.conf.urls import include, url

   urlpatterns = [
       # Other URL patterns ...
       url(r'fake/^', include('uaa_client.fake_uaa_provider.urls'))
       # More URL patterns ...
   ]

If you are using Django 1.8, you will need to additionally pass a
``namespace="fake_uaa_provider"`` keyword argument to ``include()``.

Note also that the fake server won't work properly if the web
server hosting your Django project can't handle more than one
request at a time. This generally shouldn't be a problem, since
``manage.py runserver`` doesn't have this limitation. If you're using
gunicorn to serve your app in ``DEBUG`` mode, though, you may want to
make sure that your ``WEB_CONCURRENCY`` environment variable is
set to a value greater than 1.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
