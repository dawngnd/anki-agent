"""Utility helpers for CLI output and formatting."""

import json
import sys
from typing import Any


def output_json(data: Any, pretty: bool = False) -> None:
    """Print data as JSON to stdout.

    Args:
        data: Any JSON-serializable data.
        pretty: If True, format with indentation.
    """
    indent = 2 if pretty else None
    print(json.dumps(data, indent=indent, ensure_ascii=False))


def output_error(message: str) -> None:
    """Print an error message to stderr and exit with code 1."""
    error = {"error": message}
    print(json.dumps(error, ensure_ascii=False), file=sys.stderr)
    sys.exit(1)


def output_success(message: str, data: Any = None) -> None:
    """Print a success response as JSON.

    Args:
        message: Success message.
        data: Optional data payload.
    """
    result: dict[str, Any] = {"status": "ok", "message": message}
    if data is not None:
        result["data"] = data
    output_json(result)


def confirm_action(message: str) -> bool:
    """Ask user for confirmation.

    Args:
        message: The confirmation prompt.

    Returns:
        True if user confirms, False otherwise.
    """
    try:
        response = input(f"{message} [y/N]: ").strip().lower()
        return response in ("y", "yes")
    except (EOFError, KeyboardInterrupt):
        return False
