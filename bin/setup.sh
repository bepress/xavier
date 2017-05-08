#! /bin/bash

set -e

if [ ! -d ".venv" ]; then
	virtualenv -p python3 .venv
	source .venv/bin/activate
	pip install -r test_requirements.txt
fi;
