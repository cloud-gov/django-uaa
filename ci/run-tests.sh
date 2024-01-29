#!/bin/bash

python -m venv venv
source venv/bin/activate

python -m pip install -r requirements-tests.txt

# install package in development mode
# python -m pip install --editable .

# run tests
tox
