"""Tests for CLI commands."""

import json
import unittest
from io import StringIO
from unittest.mock import patch, MagicMock

from anki_agent.cli import main


class CLITestBase(unittest.TestCase):
    """Base class for CLI tests with mocked AnkiConnect."""

    def setUp(self):
        self.patcher = patch("anki_agent.client.urllib.request.urlopen")
        self.mock_urlopen = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def mock_response(self, result, error=None):
        """Set up mock response from AnkiConnect."""
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps(
            {"result": result, "error": error}
        ).encode()
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        self.mock_urlopen.return_value = mock_resp

    def run_cli(self, args: list[str]) -> str:
        """Run CLI command and capture stdout."""
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            try:
                main(args)
            except SystemExit:
                pass
            return mock_out.getvalue()

    def run_cli_stderr(self, args: list[str]) -> str:
        """Run CLI command and capture stderr."""
        with patch("sys.stderr", new_callable=StringIO) as mock_err:
            try:
                main(args)
            except SystemExit:
                pass
            return mock_err.getvalue()


class TestPingCommand(CLITestBase):
    """Tests for the ping command."""

    def test_ping_success(self):
        self.mock_response(6)
        output = self.run_cli(["ping"])
        data = json.loads(output)
        self.assertEqual(data["status"], "ok")

    def test_ping_failure(self):
        import urllib.error
        self.mock_urlopen.side_effect = urllib.error.URLError("refused")
        output = self.run_cli_stderr(["ping"])
        data = json.loads(output)
        self.assertIn("error", data)


class TestDeckCommands(CLITestBase):
    """Tests for deck commands."""

    def test_deck_list(self):
        self.mock_response({"Default": 1, "Japanese": 2, "Science": 3})
        output = self.run_cli(["deck", "list"])
        data = json.loads(output)
        self.assertEqual(data["total"], 3)
        self.assertIn("decks", data)
        names = [d["name"] for d in data["decks"]]
        self.assertIn("Default", names)

    def test_deck_create(self):
        self.mock_response(1234567890)
        output = self.run_cli(["deck", "create", "New Deck"])
        data = json.loads(output)
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["data"]["deck_id"], 1234567890)

    def test_deck_delete_without_force(self):
        """Delete without --force should fail."""
        output = self.run_cli_stderr(["deck", "delete", "Test"])
        data = json.loads(output)
        self.assertIn("error", data)
        self.assertIn("--force", data["error"])

    def test_deck_delete_with_force(self):
        self.mock_response(None)
        output = self.run_cli(["deck", "delete", "Test", "--force"])
        data = json.loads(output)
        self.assertEqual(data["status"], "ok")


class TestNoteCommands(CLITestBase):
    """Tests for note commands."""

    def test_note_add(self):
        self.mock_response(9876543210)
        output = self.run_cli([
            "note", "add",
            "--deck", "Default",
            "--model", "Basic",
            "--front", "Hello",
            "--back", "World",
        ])
        data = json.loads(output)
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["data"]["note_id"], 9876543210)

    def test_note_add_with_tags(self):
        self.mock_response(1111111111)
        output = self.run_cli([
            "note", "add",
            "--deck", "Default",
            "--front", "Q",
            "--back", "A",
            "--tags", "vocab", "important",
        ])
        data = json.loads(output)
        self.assertEqual(data["status"], "ok")

    def test_note_find(self):
        self.mock_response([111, 222, 333])
        output = self.run_cli(["note", "find", "--query", "deck:Default"])
        data = json.loads(output)
        self.assertEqual(data["total"], 3)
        self.assertEqual(data["note_ids"], [111, 222, 333])

    def test_note_delete_without_force(self):
        output = self.run_cli_stderr(["note", "delete", "--ids", "111", "222"])
        data = json.loads(output)
        self.assertIn("--force", data["error"])

    def test_note_delete_with_force(self):
        self.mock_response(None)
        output = self.run_cli(["note", "delete", "--ids", "111", "--force"])
        data = json.loads(output)
        self.assertEqual(data["status"], "ok")

    def test_note_models(self):
        self.mock_response(["Basic", "Cloze", "Basic (and reversed card)"])
        output = self.run_cli(["note", "models"])
        data = json.loads(output)
        self.assertEqual(data["total"], 3)
        self.assertIn("Basic", data["models"])

    def test_note_model_fields(self):
        self.mock_response(["Front", "Back"])
        output = self.run_cli(["note", "model-fields", "Basic"])
        data = json.loads(output)
        self.assertEqual(data["model"], "Basic")
        self.assertEqual(data["fields"], ["Front", "Back"])


class TestCardCommands(CLITestBase):
    """Tests for card commands."""

    def test_card_find(self):
        self.mock_response([100, 200, 300])
        output = self.run_cli(["card", "find", "--query", "is:due"])
        data = json.loads(output)
        self.assertEqual(data["total"], 3)

    def test_card_suspend(self):
        self.mock_response(True)
        output = self.run_cli(["card", "suspend", "--ids", "100", "200"])
        data = json.loads(output)
        self.assertEqual(data["status"], "ok")

    def test_card_unsuspend(self):
        self.mock_response(True)
        output = self.run_cli(["card", "unsuspend", "--ids", "100"])
        data = json.loads(output)
        self.assertEqual(data["status"], "ok")


class TestTagCommands(CLITestBase):
    """Tests for tag commands."""

    def test_tag_list(self):
        self.mock_response(["vocab", "grammar", "important"])
        output = self.run_cli(["tag", "list"])
        data = json.loads(output)
        self.assertEqual(data["total"], 3)

    def test_tag_add(self):
        self.mock_response(None)
        output = self.run_cli([
            "tag", "add", "--notes", "111", "222", "--tags", "vocab important"
        ])
        data = json.loads(output)
        self.assertEqual(data["status"], "ok")

    def test_tag_find_notes(self):
        self.mock_response([111, 222])
        output = self.run_cli(["tag", "find-notes", "vocab"])
        data = json.loads(output)
        self.assertEqual(data["tag"], "vocab")
        self.assertEqual(data["total"], 2)


class TestSyncCommand(CLITestBase):
    """Tests for sync command."""

    def test_sync(self):
        self.mock_response(None)
        output = self.run_cli(["sync"])
        data = json.loads(output)
        self.assertEqual(data["status"], "ok")
        self.assertIn("Sync", data["message"])


class TestVersionCommand(CLITestBase):
    """Tests for version command."""

    def test_anki_connect_version(self):
        self.mock_response(6)
        output = self.run_cli(["version"])
        data = json.loads(output)
        self.assertEqual(data["anki_connect_version"], 6)


if __name__ == "__main__":
    unittest.main()
