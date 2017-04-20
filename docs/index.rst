.. cg-django-uaa documentation master file, created by
   sphinx-quickstart on Mon Jan 30 10:35:02 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to cg-django-uaa's documentation!
=========================================

.. toctree::
   :maxdepth: 1
   :caption: Contents

   quickstart
   backends
   developing
   changelog

This is a `cloud.gov <https://cloud.gov/>`_ UAA authentication backend
for Django. Features include:

* A handy :ref:`fake cloud.gov <fakeauth>`
  that makes it easy to log in as any user during development.

* Transparent refreshing of short-lived access tokens, ensuring that
  users are automatically logged out of the system soon after cloud.gov
  says they are unauthorized.

To get started, see the :doc:`quickstart`.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
