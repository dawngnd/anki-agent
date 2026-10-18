"""Note management commands."""

import argparse
import json
import sys
from typing import Any

from anki_agent.client import AnkiClient
from anki_agent.utils import output_json, output_success, output_error


def register(subparsers: Any) -> None:
    """Register note subcommands."""
    note_parser = subparsers.add_parser("note", help="Manage notes")
    note_sub = note_parser.add_subparsers(dest="note_command", required=True)

    # note add
    add = note_sub.add_parser("add", help="Add a new note")
    add.add_argument("--deck", required=True, help="Target deck name")
    add.add_argument(
        "--model", default="Basic", help="Note type/model name (default: Basic)"
    )
    add.add_argument("--front", help="Front field content")
    add.add_argument("--back", help="Back field content")
    add.add_argument(
        "--fields",
        help="JSON string of field name-value pairs (for custom models)",
    )
    add.add_argument(
        "--tags", nargs="*", default=[], help="Tags to add to the note"
    )
    add.add_argument(
        "--allow-duplicate",
        action="store_true",
        help="Allow adding duplicate notes",
    )

    # note add-many
    add_many = note_sub.add_parser(
        "add-many", help="Add multiple notes from JSON file or stdin"
    )
    add_many.add_argument(
        "--file",
        help="Path to JSON file with notes array. Use '-' for stdin.",
    )

    # note find
    find = note_sub.add_parser("find", help="Find notes by query")
    find.add_argument(
        "--query", required=True, help="Anki search query (e.g. 'deck:Default')"
    )
    find.add_argument(
        "--details",
        action="store_true",
        help="Include full note details (fields, tags, etc.)",
    )

    # note info
    info = note_sub.add_parser("info", help="Get detailed note information")
    info.add_argument("--ids", nargs="+", type=int, required=True, help="Note IDs")

    # note update
    update = note_sub.add_parser("update", help="Update note fields")
    update.add_argument("--id", type=int, required=True, help="Note ID")
    update.add_argument("--field", help="Field name to update")
    update.add_argument("--value", help="New field value")
    update.add_argument(
        "--fields",
        help="JSON string of field name-value pairs for bulk update",
    )

    # note delete
    delete = note_sub.add_parser("delete", help="Delete notes")
    delete.add_argument(
        "--ids", nargs="+", type=int, required=True, help="Note IDs to delete"
    )
    delete.add_argument(
        "--force",
        action="store_true",
        help="Skip confirmation prompt",
    )

    # note models
    note_sub.add_parser("models", help="List available note types/models")

    # note model-fields
    mf = note_sub.add_parser(
        "model-fields", help="List fields for a note type/model"
    )
    mf.add_argument("name", help="Model name")

    # note add-tags
    add_tags = note_sub.add_parser("add-tags", help="Add tags to notes")
    add_tags.add_argument(
        "--notes", nargs="+", type=int, required=True, help="Note IDs"
    )
    add_tags.add_argument(
        "--tags", required=True, help="Space-separated tags to add"
    )

    # note remove-tags
    rm_tags = note_sub.add_parser("remove-tags", help="Remove tags from notes")
    rm_tags.add_argument(
        "--notes", nargs="+", type=int, required=True, help="Note IDs"
    )
    rm_tags.add_argument(
        "--tags", required=True, help="Space-separated tags to remove"
    )


def execute(args: argparse.Namespace, client: AnkiClient) -> None:
    """Execute a note command."""
    cmd = args.note_command

    if cmd == "add":
        _add_note(client, args)
    elif cmd == "add-many":
        _add_many_notes(client, args)
    elif cmd == "find":
        _find_notes(client, args.query, args.details)
    elif cmd == "info":
        _get_info(client, args.ids)
    elif cmd == "update":
        _update_note(client, args)
    elif cmd == "delete":
        _delete_notes(client, args.ids, args.force)
    elif cmd == "models":
        _list_models(client)
    elif cmd == "model-fields":
        _model_fields(client, args.name)
    elif cmd == "add-tags":
        _add_tags(client, args.notes, args.tags)
    elif cmd == "remove-tags":
        _remove_tags(client, args.notes, args.tags)


def _add_note(client: AnkiClient, args: argparse.Namespace) -> None:
    """Add a single note."""
    # Build fields dict
    if args.fields:
        try:
            fields = json.loads(args.fields)
        except json.JSONDecodeError:
            output_error("--fields must be valid JSON")
            return
    elif args.front is not None:
        fields = {"Front": args.front, "Back": args.back or ""}
    else:
        output_error("Either --front/--back or --fields is required")
        return

    note: dict[str, Any] = {
        "deckName": args.deck,
        "modelName": args.model,
        "fields": fields,
        "tags": args.tags,
        "options": {
            "allowDuplicate": args.allow_duplicate,
        },
    }

    note_id = client.invoke("addNote", note=note)
    output_success("Note added", data={"note_id": note_id})


def _add_many_notes(client: AnkiClient, args: argparse.Namespace) -> None:
    """Add multiple notes from JSON file or stdin."""
    if args.file == "-" or args.file is None:
        raw = sys.stdin.read()
    else:
        with open(args.file) as f:
            raw = f.read()

    try:
        notes_data = json.loads(raw)
    except json.JSONDecodeError:
        output_error("Invalid JSON input")
        return

    if not isinstance(notes_data, list):
        output_error("Input must be a JSON array of note objects")
        return

    # Each note should have: deckName, modelName, fields, and optionally tags
    notes = []
    for item in notes_data:
        note: dict[str, Any] = {
            "deckName": item.get("deckName", item.get("deck", "Default")),
            "modelName": item.get("modelName", item.get("model", "Basic")),
            "fields": item.get("fields", {}),
            "tags": item.get("tags", []),
            "options": {
                "allowDuplicate": item.get("allowDuplicate", False),
            },
        }
        notes.append(note)

    result = client.invoke("addNotes", notes=notes)
    added = [nid for nid in result if nid is not None]
    failed = [i for i, nid in enumerate(result) if nid is None]

    output_success(
        f"Added {len(added)} of {len(notes)} notes",
        data={
            "note_ids": added,
            "failed_indices": failed,
        },
    )


def _find_notes(client: AnkiClient, query: str, details: bool) -> None:
    """Find notes matching a query."""
    note_ids = client.invoke("findNotes", query=query)

    if details and note_ids:
        notes_info = client.invoke("notesInfo", notes=note_ids)
        output_json({"notes": notes_info, "total": len(notes_info)})
    else:
        output_json({"note_ids": note_ids, "total": len(note_ids)})


def _get_info(client: AnkiClient, note_ids: list[int]) -> None:
    """Get detailed information about notes."""
    notes_info = client.invoke("notesInfo", notes=note_ids)
    output_json({"notes": notes_info, "total": len(notes_info)})


def _update_note(client: AnkiClient, args: argparse.Namespace) -> None:
    """Update fields of an existing note."""
    if args.fields:
        try:
            fields = json.loads(args.fields)
        except json.JSONDecodeError:
            output_error("--fields must be valid JSON")
            return
    elif args.field and args.value is not None:
        fields = {args.field: args.value}
    else:
        output_error("Either --field/--value or --fields is required")
        return

    client.invoke(
        "updateNoteFields",
        note={"id": args.id, "fields": fields},
    )
    output_success(f"Note {args.id} updated")


def _delete_notes(
    client: AnkiClient, note_ids: list[int], force: bool
) -> None:
    """Delete notes by ID."""
    if not force:
        output_error(
            f"Refusing to delete {len(note_ids)} note(s) without --force flag. "
            "This action is irreversible."
        )

    client.invoke("deleteNotes", notes=note_ids)
    output_success(f"Deleted {len(note_ids)} note(s)", data={"deleted_ids": note_ids})


def _list_models(client: AnkiClient) -> None:
    """List available note types (models)."""
    models = client.invoke("modelNames")
    output_json({"models": models, "total": len(models)})


def _model_fields(client: AnkiClient, name: str) -> None:
    """List fields for a note type."""
    fields = client.invoke("modelFieldNames", modelName=name)
    output_json({"model": name, "fields": fields})


def _add_tags(client: AnkiClient, note_ids: list[int], tags: str) -> None:
    """Add tags to notes."""
    # AnkiConnect addTags expects a string of note IDs joined by spaces
    notes_str = " ".join(str(nid) for nid in note_ids)
    client.invoke("addTags", notes=note_ids, tags=tags)
    output_success(f"Tags '{tags}' added to {len(note_ids)} note(s)")


def _remove_tags(client: AnkiClient, note_ids: list[int], tags: str) -> None:
    """Remove tags from notes."""
    client.invoke("removeTags", notes=note_ids, tags=tags)
    output_success(f"Tags '{tags}' removed from {len(note_ids)} note(s)")
