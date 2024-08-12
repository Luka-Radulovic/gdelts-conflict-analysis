#!/usr/bin/env bash

set -eu

rm -rf .coverage .myptest_cache .mypy_cache

isort src tests
black src tests
flake8
mypy
pytest
