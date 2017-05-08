#! /bin/bash

set -e

if [  -d ".venv" ]; then
	rm -fR .venv
fi
