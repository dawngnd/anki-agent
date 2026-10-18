"""Tag management commands."""

import argparse
from typing import Any

from anki_agent.client import AnkiClient
from anki_agent.utils import output_json, output_success


def register(subparsers: Any) -> None:
    """Register tag subcommands."""
    tag_parser = subparsers.add_parser("tag", help="Manage tags")
    tag_sub = tag_parser.add_subparsers(dest="tag_command", required=True)

    # tag list
    tag_sub.add_parser("list", help="List all tags")

    # tag add
    add = tag_sub.add_parser("add", help="Add tags to notes")
    add.add_argument(
        "--notes", nargs="+", type=int, required=True, help="Note IDs"
    )
    add.add_argument(
        "--tags", required=True, help="Space-separated tags to add"
    )

    # tag remove
    remove = tag_sub.add_parser("remove", help="Remove tags from notes")
    remove.add_argument(
        "--notes", nargs="+", type=int, required=True, help="Note IDs"
    )
    remove.add_argument(
        "--tags", required=True, help="Space-separated tags to remove"
    )

    # tag find-notes
    find = tag_sub.add_parser("find-notes", help="Find notes with a specific tag")
    find.add_argument("tag", help="Tag to search for")

    # tag clear
    clear = tag_sub.add_parser("clear", help="Remove all tags from notes")
    clear.add_argument(
        "--notes", nargs="+", type=int, required=True, help="Note IDs"
    )
    clear.add_argument(
        "--force", action="store_true", help="Skip confirmation"
    )

    # tag replace
    replace = tag_sub.add_parser("replace", help="Replace a tag across all notes")
    replace.add_argument("old_tag", help="Tag to replace")
    replace.add_argument("new_tag", help="Replacement tag")


def execute(args: argparse.Namespace, client: AnkiClient) -> None:
    """Execute a tag command."""
    cmd = args.tag_command

    if cmd == "list":
        _list_tags(client)
    elif cmd == "add":
        _add_tags(client, args.notes, args.tags)
    elif cmd == "remove":
        _remove_tags(client, args.notes, args.tags)
    elif cmd == "find-notes":
        _find_notes_by_tag(client, args.tag)
    elif cmd == "clear":
        _clear_tags(client, args.notes, args.force)
    elif cmd == "replace":
        _replace_tag(client, args.old_tag, args.new_tag)


def _list_tags(client: AnkiClient) -> None:
    """List all tags in the collection."""
    tags = client.invoke("getTags")
    output_json({"tags": tags, "total": len(tags)})


def _add_tags(client: AnkiClient, note_ids: list[int], tags: str) -> None:
    """Add tags to notes."""
    client.invoke("addTags", notes=note_ids, tags=tags)
    output_success(f"Tags '{tags}' added to {len(note_ids)} note(s)")


def _remove_tags(client: AnkiClient, note_ids: list[int], tags: str) -> None:
    """Remove tags from notes."""
    client.invoke("removeTags", notes=note_ids, tags=tags)
    output_success(f"Tags '{tags}' removed from {len(note_ids)} note(s)")


def _find_notes_by_tag(client: AnkiClient, tag: str) -> None:
    """Find notes that have a specific tag."""
    note_ids = client.invoke("findNotes", query=f"tag:{tag}")
    output_json({"tag": tag, "note_ids": note_ids, "total": len(note_ids)})


def _clear_tags(
    client: AnkiClient, note_ids: list[int], force: bool
) -> None:
    """Remove all tags from notes."""
    from anki_agent.utils import output_error

    if not force:
        output_error(
            f"Refusing to clear all tags from {len(note_ids)} note(s) "
            "without --force flag."
        )

    # Get current tags for each note, then remove them all
    notes_info = client.invoke("notesInfo", notes=note_ids)
    for note in notes_info:
        if note.get("tags"):
            tags_str = " ".join(note["tags"])
            client.invoke("removeTags", notes=[note["noteId"]], tags=tags_str)

    output_success(f"All tags cleared from {len(note_ids)} note(s)")


def _replace_tag(client: AnkiClient, old_tag: str, new_tag: str) -> None:
    """Replace a tag across all notes that have it."""
    client.invoke("replaceTags", notes=[], tag_to_replace=old_tag, replace_with_tag=new_tag)
    # The above may not work in all AnkiConnect versions, so use manual approach:
    note_ids = client.invoke("findNotes", query=f"tag:{old_tag}")
    if note_ids:
        client.invoke("addTags", notes=note_ids, tags=new_tag)
        client.invoke("removeTags", notes=note_ids, tags=old_tag)

    output_success(
        f"Replaced tag '{old_tag}' with '{new_tag}' on {len(note_ids)} note(s)"
    )
