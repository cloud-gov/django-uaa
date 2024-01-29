#!/bin/bash

python -m venv venv
source venv/bin/activate

python -m pip install -r requirements-tests.txt

# run tests in development mode
tox --develop
