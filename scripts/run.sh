#!/bin/bash

set -e

VENV_DIR=".venv"
APP_FILE="app/main.py"

cd "$(dirname "$0")/.."

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"

    echo "Activating virtual environment..."
    source "$VENV_DIR/bin/activate"

    echo "Installing requirements..."
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
else
    echo "Using existing virtual environment..."
    source "$VENV_DIR/bin/activate"
fi

echo "Starting Streamlit application..."
PYTHONPATH="$PWD" streamlit run "$APP_FILE"