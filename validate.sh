#!/usr/bin/env bash
set -ex

ruff format --check .
ruff check .
mypy --install-types --non-interactive dataall_sdk
pylint dataall_sdk/
doc8 --ignore-path docs/source/stubs --max-line-length 1000 docs/source
poetry check --lock
