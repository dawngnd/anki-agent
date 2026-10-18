"""Deck management commands."""

import argparse
from typing import Any

from anki_agent.client import AnkiClient
from anki_agent.utils import output_json, output_success, output_error


def register(subparsers: Any) -> None:
    """Register deck subcommands."""
    deck_parser = subparsers.add_parser("deck", help="Manage decks")
    deck_sub = deck_parser.add_subparsers(dest="deck_command", required=True)

    # deck list
    deck_sub.add_parser("list", help="List all decks with IDs")

    # deck create
    create = deck_sub.add_parser("create", help="Create a new deck")
    create.add_argument("name", help="Deck name (use :: for nested, e.g. 'Parent::Child')")

    # deck delete
    delete = deck_sub.add_parser("delete", help="Delete a deck")
    delete.add_argument("name", help="Deck name to delete")
    delete.add_argument(
        "--cards-too",
        action="store_true",
        default=True,
        help="Also delete cards in the deck (default: True)",
    )
    delete.add_argument(
        "--force",
        action="store_true",
        help="Skip confirmation prompt",
    )

    # deck stats
    stats = deck_sub.add_parser("stats", help="Get deck statistics")
    stats.add_argument("name", help="Deck name")

    # deck rename
    rename = deck_sub.add_parser("rename", help="Rename a deck")
    rename.add_argument("old_name", help="Current deck name")
    rename.add_argument("new_name", help="New deck name")


def execute(args: argparse.Namespace, client: AnkiClient) -> None:
    """Execute a deck command."""
    cmd = args.deck_command

    if cmd == "list":
        _list_decks(client)
    elif cmd == "create":
        _create_deck(client, args.name)
    elif cmd == "delete":
        _delete_deck(client, args.name, args.cards_too, args.force)
    elif cmd == "stats":
        _get_stats(client, args.name)
    elif cmd == "rename":
        _rename_deck(client, args.old_name, args.new_name)


def _list_decks(client: AnkiClient) -> None:
    """List all decks with their IDs."""
    result = client.invoke("deckNamesAndIds")
    decks = [{"name": name, "id": deck_id} for name, deck_id in result.items()]
    output_json({"decks": decks, "total": len(decks)})


def _create_deck(client: AnkiClient, name: str) -> None:
    """Create a new deck."""
    deck_id = client.invoke("createDeck", deck=name)
    output_success(f"Deck '{name}' created", data={"deck_id": deck_id})


def _delete_deck(
    client: AnkiClient, name: str, cards_too: bool, force: bool
) -> None:
    """Delete a deck."""
    if not force:
        output_error(
            f"Refusing to delete deck '{name}' without --force flag. "
            "This action is irreversible."
        )

    client.invoke("deleteDecks", decks=[name], cardsToo=cards_too)
    output_success(f"Deck '{name}' deleted")


def _get_stats(client: AnkiClient, name: str) -> None:
    """Get deck statistics."""
    # First get deck ID
    decks = client.invoke("deckNamesAndIds")
    deck_id = decks.get(name)
    if deck_id is None:
        output_error(f"Deck '{name}' not found")

    stats = client.invoke("getDeckStats", decks=[deck_id])
    output_json(stats)


def _rename_deck(client: AnkiClient, old_name: str, new_name: str) -> None:
    """Rename a deck."""
    # AnkiConnect doesn't have a direct rename action,
    # but we can use changeDeck or the internal rename method.
    # Using the Anki GUI action approach:
    decks = client.invoke("deckNamesAndIds")
    if old_name not in decks:
        output_error(f"Deck '{old_name}' not found")

    # Create new deck and move cards
    client.invoke("createDeck", deck=new_name)

    # Find all cards in old deck and move them
    cards = client.invoke("findCards", query=f'"deck:{old_name}"')
    if cards:
        client.invoke("changeDeck", cards=cards, deck=new_name)

    # Delete old deck
    client.invoke("deleteDecks", decks=[old_name], cardsToo=False)
    output_success(f"Deck renamed from '{old_name}' to '{new_name}'")
