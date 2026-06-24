#!/bin/bash

set -e

cd "$(dirname "$0")/.."

source .venv/bin/activate

PYTHONPATH="$PWD" python3 tests/run_tests/run_bpm_test.py