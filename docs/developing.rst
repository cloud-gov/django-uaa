Developing cg-django-uaa
========================

.. important::

    This section is about developing cg-django-uaa
    itself, not using it in your Django project. For
    details on the latter, see the :doc:`quickstart`.

.. highlight:: none

First, clone the git repository::

    git clone https://github.com/cloud-gov/cg-django-uaa

Then create a virtualenv for the project and install
development dependencies::

    python -m venv venv
    source venv/bin/activate
    python -m pip install -r requirements-dev.txt

Then install cg-django-uaa in development mode::

    python -m pip install -e .

Using the example app
~~~~~~~~~~~~~~~~~~~~~

An example Django project provides a trivial integration with
cg-django-uaa and can be used to manually ensure that everything
works as expected.

To use it, run the following from the root of the repository::

    cd example
    python manage.py migrate
    python manage.py createsuperuser --username foo --email foo@example.org --noinput
    python manage.py runserver

At this point you should be able to visit the locally-hosted project
and login to fake cloud.gov as foo@example.org.

If you'd like to modify any of the example app's settings, you can
do so by creating an ``example/example/settings_local.py`` file;
any settings defined there will override the ones in
``example/example/settings.py``.

Running tests
~~~~~~~~~~~~~

You can run this test against all envionments in the test matrix
with::

    tox

or against specific versions, for instance python 3.8 with django 3.1::

    tox -e py38-django31


Formatting code
~~~~~~~~~~~~~~~

Code should be formated with `black
<https://black.readthedocs.io/en/stable/>`_. Because we have configuration in our ``pyproject.toml``,
you can (and should!) run this before committing::

    black .

Writing documentation
~~~~~~~~~~~~~~~~~~~~~

If you want to work on documentation, you can run the development
documentation server with::

    python test.py devdocs
