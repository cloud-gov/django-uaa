#!/bin/bash

python -m venv venv
source ./venv/bin/activate

python -m pip install -r requirements-tests.txt
python -m pip install -e .

# run tests
tox
