#!/bin/bash

TAG=$(git describe --tags)
echo "$TAG" > tag

# Install build module
python -m pip install build

# Build release
python -m build --sdist
