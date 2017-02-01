#! /bin/bash

# This script can be used to rebuild the documentation and push it to
# the 'built-docs' branch, which can then be deployed through a service
# like federalist.18f.gov.

set -e

cd docs
rm -rf _build
make html
cd ..

rm -rf built-docs-branch
git fetch origin built-docs
git clone -b built-docs . built-docs-branch
cd built-docs-branch
git rm -rf --ignore-unmatch .
cp -R ../docs/_build/html/ .
cp ../.travis.yml .
git add .
git commit -m "Rebuild docs." || echo "Looks like the site did not change."
git push origin built-docs
cd ..
git push origin built-docs
rm -rf built-docs-branch
