"""Card management commands."""

import argparse
from typing import Any

from anki_agent.client import AnkiClient
from anki_agent.utils import output_json, output_success, output_error


def register(subparsers: Any) -> None:
    """Register card subcommands."""
    card_parser = subparsers.add_parser("card", help="Manage cards")
    card_sub = card_parser.add_subparsers(dest="card_command", required=True)

    # card find
    find = card_sub.add_parser("find", help="Find cards by query")
    find.add_argument(
        "--query", required=True, help="Anki search query (e.g. 'is:due')"
    )

    # card info
    info = card_sub.add_parser("info", help="Get detailed card information")
    info.add_argument("--ids", nargs="+", type=int, required=True, help="Card IDs")

    # card suspend
    suspend = card_sub.add_parser("suspend", help="Suspend cards")
    suspend.add_argument(
        "--ids", nargs="+", type=int, required=True, help="Card IDs to suspend"
    )

    # card unsuspend
    unsuspend = card_sub.add_parser("unsuspend", help="Unsuspend cards")
    unsuspend.add_argument(
        "--ids", nargs="+", type=int, required=True, help="Card IDs to unsuspend"
    )

    # card due
    due = card_sub.add_parser("due", help="List cards due for review")
    due.add_argument(
        "--deck", help="Filter by deck name (optional)"
    )
    due.add_argument(
        "--limit", type=int, default=100, help="Maximum number of cards (default: 100)"
    )

    # card move
    move = card_sub.add_parser("move", help="Move cards to a different deck")
    move.add_argument(
        "--ids", nargs="+", type=int, required=True, help="Card IDs to move"
    )
    move.add_argument("--deck", required=True, help="Target deck name")


def execute(args: argparse.Namespace, client: AnkiClient) -> None:
    """Execute a card command."""
    cmd = args.card_command

    if cmd == "find":
        _find_cards(client, args.query)
    elif cmd == "info":
        _get_info(client, args.ids)
    elif cmd == "suspend":
        _suspend_cards(client, args.ids)
    elif cmd == "unsuspend":
        _unsuspend_cards(client, args.ids)
    elif cmd == "due":
        _due_cards(client, getattr(args, "deck", None), args.limit)
    elif cmd == "move":
        _move_cards(client, args.ids, args.deck)


def _find_cards(client: AnkiClient, query: str) -> None:
    """Find cards matching a query."""
    card_ids = client.invoke("findCards", query=query)
    output_json({"card_ids": card_ids, "total": len(card_ids)})


def _get_info(client: AnkiClient, card_ids: list[int]) -> None:
    """Get detailed information about cards."""
    cards_info = client.invoke("cardsInfo", cards=card_ids)
    output_json({"cards": cards_info, "total": len(cards_info)})


def _suspend_cards(client: AnkiClient, card_ids: list[int]) -> None:
    """Suspend cards."""
    client.invoke("suspend", cards=card_ids)
    output_success(f"Suspended {len(card_ids)} card(s)", data={"card_ids": card_ids})


def _unsuspend_cards(client: AnkiClient, card_ids: list[int]) -> None:
    """Unsuspend cards."""
    client.invoke("unsuspend", cards=card_ids)
    output_success(f"Unsuspended {len(card_ids)} card(s)", data={"card_ids": card_ids})


def _due_cards(
    client: AnkiClient, deck: str | None, limit: int
) -> None:
    """List cards due for review."""
    query = "is:due"
    if deck:
        query = f'"deck:{deck}" is:due'

    card_ids = client.invoke("findCards", query=query)
    card_ids = card_ids[:limit]

    if card_ids:
        cards_info = client.invoke("cardsInfo", cards=card_ids)
        output_json({
            "cards": cards_info,
            "total_due": len(card_ids),
            "showing": len(cards_info),
        })
    else:
        output_json({"cards": [], "total_due": 0, "showing": 0})


def _move_cards(
    client: AnkiClient, card_ids: list[int], deck: str
) -> None:
    """Move cards to a different deck."""
    client.invoke("changeDeck", cards=card_ids, deck=deck)
    output_success(
        f"Moved {len(card_ids)} card(s) to '{deck}'",
        data={"card_ids": card_ids, "deck": deck},
    )
