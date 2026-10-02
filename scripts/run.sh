#!/bin/bash

set -e


# ---------------------------------------------------------
# Project root
# ---------------------------------------------------------

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$PROJECT_ROOT"


# ---------------------------------------------------------
# Virtual environment
# ---------------------------------------------------------

if [ ! -d ".venv" ]; then

    echo "Creating virtual environment..."

    python -m venv .venv

fi


# ---------------------------------------------------------
# Activate virtual environment
# ---------------------------------------------------------

echo "Activating virtual environment..."

source .venv/bin/activate

echo "Acitaved."

# ---------------------------------------------------------
# Python path
# ---------------------------------------------------------

export PYTHONPATH="$PWD/src"


# ---------------------------------------------------------
# Dependencies
# ---------------------------------------------------------

echo "Checking dependencies..."

if ! python -c "import chromadb, ollama, streamlit" 2>/dev/null; then

    echo "Installing dependencies..."

    pip install -r requirements.txt

fi


# ---------------------------------------------------------
# Ollama
# ---------------------------------------------------------

if pgrep -x "ollama" > /dev/null; then

    echo "Ollama is already running."

else

    echo "Starting Ollama..."

    ollama serve > /tmp/voltix-ollama.log 2>&1 &

    sleep 2

    echo "Ollama started."

fi


echo
echo "Environment setup completed."
echo