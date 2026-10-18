"""CLI entry point for anki-agent.

Usage:
    anki-agent [--url URL] [--api-key KEY] <command> <subcommand> [options]

Environment variables:
    ANKI_CONNECT_URL      AnkiConnect server URL (default: http://localhost:8765)
    ANKI_CONNECT_API_KEY  API key for AnkiConnect authentication
"""

import argparse
import sys

from anki_agent import __version__
from anki_agent.client import AnkiClient, AnkiConnectError, AnkiConnectionError
from anki_agent.commands import deck, note, card, tag, media
from anki_agent.utils import output_error, output_json, output_success


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser with all subcommands."""
    parser = argparse.ArgumentParser(
        prog="anki-agent",
        description="CLI tools for managing Anki flashcards via AnkiConnect",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"anki-agent {__version__}",
    )
    parser.add_argument(
        "--url",
        help="AnkiConnect URL (default: http://localhost:8765)",
    )
    parser.add_argument(
        "--api-key",
        help="AnkiConnect API key",
    )

    subparsers = parser.add_subparsers(dest="command")

    # Register command modules
    deck.register(subparsers)
    note.register(subparsers)
    card.register(subparsers)
    tag.register(subparsers)
    media.register(subparsers)

    # Top-level commands
    subparsers.add_parser("ping", help="Check AnkiConnect connection")
    subparsers.add_parser("sync", help="Trigger sync with AnkiWeb")
    subparsers.add_parser("version", help="Show AnkiConnect version")
    subparsers.add_parser("profiles", help="List available Anki profiles")

    return parser


def main(argv: list[str] | None = None) -> None:
    """Main entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Create client
    client = AnkiClient(url=args.url, api_key=args.api_key)

    try:
        if args.command == "ping":
            _ping(client)
        elif args.command == "sync":
            _sync(client)
        elif args.command == "version":
            _version(client)
        elif args.command == "profiles":
            _profiles(client)
        elif args.command == "deck":
            deck.execute(args, client)
        elif args.command == "note":
            note.execute(args, client)
        elif args.command == "card":
            card.execute(args, client)
        elif args.command == "tag":
            tag.execute(args, client)
        elif args.command == "media":
            media.execute(args, client)
        else:
            parser.print_help()
            sys.exit(1)
    except AnkiConnectionError as exc:
        output_error(str(exc))
    except AnkiConnectError as exc:
        output_error(f"AnkiConnect error: {exc}")
    except KeyboardInterrupt:
        sys.exit(130)


def _ping(client: AnkiClient) -> None:
    """Check AnkiConnect connection."""
    if client.ping():
        output_success("AnkiConnect is reachable")
    else:
        output_error("Cannot connect to AnkiConnect")


def _sync(client: AnkiClient) -> None:
    """Trigger sync with AnkiWeb."""
    client.invoke("sync")
    output_success("Sync triggered")


def _version(client: AnkiClient) -> None:
    """Show AnkiConnect version."""
    version = client.invoke("version")
    output_json({"anki_connect_version": version})


def _profiles(client: AnkiClient) -> None:
    """List available Anki profiles."""
    profiles = client.invoke("getProfiles")
    output_json({"profiles": profiles})


if __name__ == "__main__":
    main()
