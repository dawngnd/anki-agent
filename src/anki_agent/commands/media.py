"""Media file management commands."""

import argparse
import base64
from pathlib import Path
from typing import Any

from anki_agent.client import AnkiClient
from anki_agent.utils import output_json, output_success, output_error


def register(subparsers: Any) -> None:
    """Register media subcommands."""
    media_parser = subparsers.add_parser("media", help="Manage media files")
    media_sub = media_parser.add_subparsers(dest="media_command", required=True)

    # media store
    store = media_sub.add_parser("store", help="Upload a media file to Anki")
    store.add_argument("--filename", required=True, help="Filename in Anki media folder")
    store.add_argument("--path", help="Path to local file to upload")
    store.add_argument("--url", help="URL to download file from")
    store.add_argument("--data", help="Base64-encoded file data")

    # media retrieve
    retrieve = media_sub.add_parser("retrieve", help="Get a media file from Anki")
    retrieve.add_argument("--filename", required=True, help="Filename in Anki media folder")
    retrieve.add_argument(
        "--output",
        help="Output file path (default: print base64 to stdout)",
    )

    # media delete
    delete = media_sub.add_parser("delete", help="Delete a media file")
    delete.add_argument("--filename", required=True, help="Filename to delete")
    delete.add_argument("--force", action="store_true", help="Skip confirmation")

    # media list
    media_sub.add_parser(
        "list", help="List media files (matching a pattern)"
    ).add_argument(
        "--pattern", default="*", help="Filename pattern (default: '*')"
    )


def execute(args: argparse.Namespace, client: AnkiClient) -> None:
    """Execute a media command."""
    cmd = args.media_command

    if cmd == "store":
        _store_media(client, args)
    elif cmd == "retrieve":
        _retrieve_media(client, args.filename, getattr(args, "output", None))
    elif cmd == "delete":
        _delete_media(client, args.filename, args.force)
    elif cmd == "list":
        _list_media(client, args.pattern)


def _store_media(client: AnkiClient, args: argparse.Namespace) -> None:
    """Store a media file in Anki's media folder."""
    if args.url:
        # Store from URL
        result = client.invoke(
            "storeMediaFile",
            filename=args.filename,
            url=args.url,
        )
    elif args.path:
        # Store from local file
        path = Path(args.path)
        if not path.exists():
            output_error(f"File not found: {args.path}")
            return

        data = base64.b64encode(path.read_bytes()).decode("utf-8")
        result = client.invoke(
            "storeMediaFile",
            filename=args.filename,
            data=data,
        )
    elif args.data:
        # Store from base64 data
        result = client.invoke(
            "storeMediaFile",
            filename=args.filename,
            data=args.data,
        )
    else:
        output_error("One of --path, --url, or --data is required")
        return

    output_success(f"Media file '{args.filename}' stored", data={"filename": result})


def _retrieve_media(
    client: AnkiClient, filename: str, output_path: str | None
) -> None:
    """Retrieve a media file from Anki."""
    data = client.invoke("retrieveMediaFile", filename=filename)

    if data is False:
        output_error(f"Media file '{filename}' not found")
        return

    if output_path:
        # Write to file
        file_bytes = base64.b64decode(data)
        Path(output_path).write_bytes(file_bytes)
        output_success(
            f"Media file '{filename}' saved to '{output_path}'",
            data={"filename": filename, "output": output_path, "size": len(file_bytes)},
        )
    else:
        # Output base64 data
        output_json({"filename": filename, "data": data})


def _delete_media(client: AnkiClient, filename: str, force: bool) -> None:
    """Delete a media file."""
    if not force:
        output_error(
            f"Refusing to delete media file '{filename}' without --force flag."
        )

    client.invoke("deleteMediaFile", filename=filename)
    output_success(f"Media file '{filename}' deleted")


def _list_media(client: AnkiClient, pattern: str) -> None:
    """List media files matching a pattern."""
    files = client.invoke("getMediaFilesNames", pattern=pattern)
    output_json({"files": files, "total": len(files)})
