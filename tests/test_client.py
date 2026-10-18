"""Tests for AnkiConnect client."""

import json
import unittest
from unittest.mock import patch, MagicMock

from anki_agent.client import AnkiClient, AnkiConnectError, AnkiConnectionError


class TestAnkiClient(unittest.TestCase):
    """Tests for AnkiClient."""

    def setUp(self):
        self.client = AnkiClient(url="http://localhost:8765")

    @patch("anki_agent.client.urllib.request.urlopen")
    def test_invoke_success(self, mock_urlopen):
        """Test successful API call."""
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(
            {"result": ["Default", "Test"], "error": None}
        ).encode()
        mock_response.__enter__ = lambda s: s
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response

        result = self.client.invoke("deckNames")
        self.assertEqual(result, ["Default", "Test"])

    @patch("anki_agent.client.urllib.request.urlopen")
    def test_invoke_with_params(self, mock_urlopen):
        """Test API call with parameters."""
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(
            {"result": 1234567890, "error": None}
        ).encode()
        mock_response.__enter__ = lambda s: s
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response

        result = self.client.invoke("createDeck", deck="Test Deck")
        self.assertEqual(result, 1234567890)

        # Verify the request body
        call_args = mock_urlopen.call_args
        request = call_args[0][0]
        body = json.loads(request.data.decode())
        self.assertEqual(body["action"], "createDeck")
        self.assertEqual(body["version"], 6)
        self.assertEqual(body["params"]["deck"], "Test Deck")

    @patch("anki_agent.client.urllib.request.urlopen")
    def test_invoke_error(self, mock_urlopen):
        """Test API call that returns an error."""
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(
            {"result": None, "error": "deck was not found"}
        ).encode()
        mock_response.__enter__ = lambda s: s
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response

        with self.assertRaises(AnkiConnectError) as ctx:
            self.client.invoke("getDeckStats", decks=[99999])
        self.assertIn("deck was not found", str(ctx.exception))

    @patch("anki_agent.client.urllib.request.urlopen")
    def test_invoke_connection_error(self, mock_urlopen):
        """Test connection error when Anki is not running."""
        import urllib.error

        mock_urlopen.side_effect = urllib.error.URLError("Connection refused")

        with self.assertRaises(AnkiConnectionError) as ctx:
            self.client.invoke("version")
        self.assertIn("Cannot connect", str(ctx.exception))

    @patch("anki_agent.client.urllib.request.urlopen")
    def test_ping_success(self, mock_urlopen):
        """Test ping when AnkiConnect is available."""
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(
            {"result": 6, "error": None}
        ).encode()
        mock_response.__enter__ = lambda s: s
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response

        self.assertTrue(self.client.ping())

    @patch("anki_agent.client.urllib.request.urlopen")
    def test_ping_failure(self, mock_urlopen):
        """Test ping when AnkiConnect is unavailable."""
        import urllib.error

        mock_urlopen.side_effect = urllib.error.URLError("Connection refused")

        self.assertFalse(self.client.ping())

    def test_api_key_in_request(self):
        """Test that API key is included in request body."""
        client = AnkiClient(api_key="test-secret-key")

        with patch("anki_agent.client.urllib.request.urlopen") as mock_urlopen:
            mock_response = MagicMock()
            mock_response.read.return_value = json.dumps(
                {"result": 6, "error": None}
            ).encode()
            mock_response.__enter__ = lambda s: s
            mock_response.__exit__ = MagicMock(return_value=False)
            mock_urlopen.return_value = mock_response

            client.invoke("version")

            call_args = mock_urlopen.call_args
            request = call_args[0][0]
            body = json.loads(request.data.decode())
            self.assertEqual(body["key"], "test-secret-key")

    def test_no_api_key_by_default(self):
        """Test that no key is sent when api_key is not set."""
        client = AnkiClient()

        with patch("anki_agent.client.urllib.request.urlopen") as mock_urlopen:
            mock_response = MagicMock()
            mock_response.read.return_value = json.dumps(
                {"result": 6, "error": None}
            ).encode()
            mock_response.__enter__ = lambda s: s
            mock_response.__exit__ = MagicMock(return_value=False)
            mock_urlopen.return_value = mock_response

            client.invoke("version")

            call_args = mock_urlopen.call_args
            request = call_args[0][0]
            body = json.loads(request.data.decode())
            self.assertNotIn("key", body)

    def test_env_url(self):
        """Test URL from environment variable."""
        with patch.dict("os.environ", {"ANKI_CONNECT_URL": "http://custom:9999"}):
            client = AnkiClient()
            self.assertEqual(client.url, "http://custom:9999")

    def test_env_api_key(self):
        """Test API key from environment variable."""
        with patch.dict("os.environ", {"ANKI_CONNECT_API_KEY": "env-key"}):
            client = AnkiClient()
            self.assertEqual(client.api_key, "env-key")


if __name__ == "__main__":
    unittest.main()
