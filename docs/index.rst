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

This is a cloud.gov UAA authentication backend for Django. It also
includes a handy "fake cloud.gov" that makes it easy to log in
as any user during development.

.. warning:: This package is in a very early stage of development
   and its settings and/or API will likely change in the near future.
   Use it at your own risk!

   For example, at present, the backend only allows users to log in who
   have existing Django ``User`` models associated with their cloud.gov
   email addresses in the database.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
