#!/bin/bash

python -m venv venv
source venv/bin/activate

TAG=$(git describe --tags)

python -m pip install -r requirements-tests.txt

# run tests on release
tox --installpkg "dist/cg-django-uaa-$TAG.tar.gz"
