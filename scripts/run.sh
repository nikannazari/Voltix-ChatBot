#!/bin/bash

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$PROJECT_ROOT"


# ---------------------------------------------------------
# Python virtual environment
# ---------------------------------------------------------

if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."

    python -m venv .venv
fi


echo "Activating virtual environment..."

source .venv/bin/activate


# ---------------------------------------------------------
# Python path
# ---------------------------------------------------------

export PYTHONPATH="$PWD/src"


# ---------------------------------------------------------
# Dependencies
# ---------------------------------------------------------

if ! python -c "import chromadb, ollama, streamlit" 2>/dev/null; then
    echo "Installing project dependencies..."

    pip install -r requirements.txt
fi


# ---------------------------------------------------------
# Ollama
# ---------------------------------------------------------

if ! pgrep -x "ollama" > /dev/null; then
    echo "Starting Ollama..."

    ollama serve > /tmp/ollama.log 2>&1 &

    sleep 2
fi


# ---------------------------------------------------------
# Start application
# ---------------------------------------------------------

echo
echo "Starting Voltix Project Chatbot..."
echo

python -m project_chatbot.main