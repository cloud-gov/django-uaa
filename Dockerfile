FROM python:3.10

# This Dockerfile manually installs cg-django-uaa from a built
# distribution and sets up the example app to run. It can be used
# to verify that everything about the packaging of cg-django-uaa is
# working properly (e.g., that important data files aren't being left
# out of the built distribution).

ARG version

ARG django_version

RUN pip install django==${django_version}

COPY requirements-tests.txt /

RUN pip install -r /requirements-tests.txt

COPY dist/cg_django_uaa-${version}.tar.gz /

WORKDIR /

RUN pip install cg_django_uaa-${version}.tar.gz && \
  python -m uaa_client.runtests

COPY example /example

# Remove existing database from local testing, if any,
# otherwise superuser creation below will fail
RUN rm /example/db.sqlite3 || true

WORKDIR /example

RUN python manage.py migrate && \
  python manage.py createsuperuser --noinput \
  --username foo --email foo@example.org

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000
