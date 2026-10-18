#!/usr/bin/env bash
# Quick setup script for anki-agent skill
# Activates venv and verifies connection

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"

# Activate venv
if [ -f "$VENV_DIR/bin/activate" ]; then
    source "$VENV_DIR/bin/activate"
else
    echo '{"error": "Virtual environment not found. Run: cd '"$PROJECT_DIR"' && python3 -m venv .venv && source .venv/bin/activate && pip install -e ."}'
    exit 1
fi

# Check connection
anki-agent ping
