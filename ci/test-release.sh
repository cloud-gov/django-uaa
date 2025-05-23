#!/bin/bash

python -m venv venv
source venv/bin/activate

TAG=$(git describe --tags | sed -e 's/^v//')

python -m pip install -r requirements-tests.txt

# run tests on release
tox --installpkg "dist/cg_django_uaa-$TAG.tar.gz"
