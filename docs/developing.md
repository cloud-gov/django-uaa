# Developing cg-django-uaa

> **Important**
> This section is about developing cg-django-uaa itself, not using it in
your Django project. For details on the latter, see the
[Quick start guide](./quickstart.md)

First, clone the git repository:

```shell
git clone https://github.com/cloud-gov/cg-django-uaa
```

Then create a virtualenv for the project and install development
dependencies:

```shell
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements-dev.txt
```

Then install cg-django-uaa in development mode:

```shell
python -m pip install --editable .
```

## Using the example app

An example Django project provides a trivial integration with
cg-django-uaa and can be used to manually ensure that everything works
as expected.

To use it, run the following from the root of the repository:

```shell
cd example
python manage.py migrate
python manage.py createsuperuser --username foo --email foo@example.org --noinput
python manage.py runserver
```

At this point you should be able to visit the locally-hosted project and
login to fake cloud.gov as <foo@example.org>.

If you\'d like to modify any of the example app\'s settings, you can do
so by creating an `example/example/settings_local.py` file; any settings
defined there will override the ones in `example/example/settings.py`.

## Running tests

You can run this test against all envionments in the test matrix with:

```shell
tox
```

or against specific versions, for instance Python 3.10 with Django 4.2:

```shell
tox -e py310-django42
```

## Formatting code

Code should be formated with
[black](https://black.readthedocs.io/en/stable/). Because we have
configuration in our `pyproject.toml`, you can (and should!) run this
before committing:

```shell
black .
```

## Writing documentation

If you want to work on documentation, you can run the development
documentation server with:

```shell
python test.py devdocs
```
