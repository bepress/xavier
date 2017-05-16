#! /bin/bash

set -e

python setup.py sdist upload -r pypi
