"""AnkiConnect HTTP client.

Communicates with Anki Desktop via the AnkiConnect add-on REST API
at http://localhost:8765 (default).
"""

import json
import os
import urllib.request
import urllib.error
from typing import Any, Optional

ANKI_CONNECT_URL = "http://localhost:8765"


class AnkiConnectError(Exception):
    """Error returned by the AnkiConnect API."""


class AnkiConnectionError(Exception):
    """Cannot connect to AnkiConnect (Anki not running or add-on missing)."""


class AnkiClient:
    """HTTP client for AnkiConnect API.

    Args:
        url: AnkiConnect server URL. Defaults to ANKI_CONNECT_URL or
             the ANKI_CONNECT_URL environment variable.
        api_key: Optional API key for AnkiConnect authentication.
                 Falls back to ANKI_CONNECT_API_KEY environment variable.
    """

    def __init__(
        self,
        url: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> None:
        self.url = url or os.environ.get("ANKI_CONNECT_URL", ANKI_CONNECT_URL)
        self.api_key = api_key or os.environ.get("ANKI_CONNECT_API_KEY")

    def invoke(self, action: str, **params: Any) -> Any:
        """Send a request to AnkiConnect and return the result.

        Args:
            action: The AnkiConnect action name (e.g., 'deckNames').
            **params: Parameters for the action.

        Returns:
            The result from AnkiConnect.

        Raises:
            AnkiConnectError: If AnkiConnect returns an error.
            AnkiConnectionError: If unable to connect to AnkiConnect.
        """
        request_body: dict[str, Any] = {
            "action": action,
            "version": 6,
        }
        if params:
            request_body["params"] = params
        if self.api_key:
            request_body["key"] = self.api_key

        data = json.dumps(request_body).encode("utf-8")
        request = urllib.request.Request(
            self.url,
            data=data,
            headers={"Content-Type": "application/json"},
        )

        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                result = json.loads(response.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            raise AnkiConnectionError(
                f"Cannot connect to AnkiConnect at {self.url}. "
                "Is Anki running with AnkiConnect add-on installed?"
            ) from exc

        if result.get("error"):
            raise AnkiConnectError(result["error"])

        return result.get("result")

    def ping(self) -> bool:
        """Check if AnkiConnect is reachable.

        Returns:
            True if AnkiConnect responds, False otherwise.
        """
        try:
            version = self.invoke("version")
            return version is not None
        except (AnkiConnectError, AnkiConnectionError):
            return False

    def multi(self, actions: list[dict[str, Any]]) -> list[Any]:
        """Execute multiple actions in a single request.

        Args:
            actions: List of action dicts, each with 'action' and optional 'params'.

        Returns:
            List of results, one per action.
        """
        return self.invoke("multi", actions=actions)
