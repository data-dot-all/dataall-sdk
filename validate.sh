#!/usr/bin/env bash
set -ex

ruff format --check .
ruff check .
mypy --install-types --non-interactive dataall_sdk
pylint -j 0 --disable=all --enable=R0911,R0912,R0913,R0915 --fail-under=9 dataall_sdk/
doc8 --ignore-path docs/source/stubs --max-line-length 1000 docs/source
poetry check --lock
