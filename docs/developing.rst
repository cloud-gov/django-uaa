Developing cg-django-uaa
========================

.. important::

    This section is about developing cg-django-uaa
    itself, not using it in your Django project. For
    details on the latter, see the :ref:`quickstart`.

.. highlight:: none

First, clone the git repository::

    git clone https://github.com/18F/cg-django-uaa

Then create a virtualenv for the project and install
development dependencies::

    virtualenv -p python3 venv
    source venv/bin/activate
    pip install -r requirements-dev.txt

At this point, you can run all the tests with code coverage
and linting::

    python setup.py ultratest

Note that this command will fail if any tests do not pass, if
there are any linting warnings, or if code coverage is not at
100%.

If you want to work on documentation, you can run the development
documentation server with::

    python setup.py devdocs
