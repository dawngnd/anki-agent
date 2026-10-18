---
name: anki-flashcard-management
description: >-
  Manages Anki flashcards via the anki-agent CLI tools. Use when the user asks
  to create, edit, delete, search, or organize Anki flashcards and decks.
  Use when the user wants to generate study cards from notes, documents, or
  conversations. Use when managing tags, media, or syncing with AnkiWeb.
---

# Anki Flashcard Management

## Overview

This skill enables the AI agent to manage Anki flashcards through the
`anki-agent` CLI tool. The tool communicates with Anki Desktop via the
AnkiConnect add-on (HTTP API at `localhost:8765`).

**All CLI outputs are JSON** — parse them programmatically, never guess.

## Prerequisites

Before using any command, verify these prerequisites:

1. **Anki Desktop** must be running on the user's machine
2. **AnkiConnect add-on** must be installed (code: `2055492159`)
3. The `anki-agent` CLI must be available

### Quick Health Check

```bash
# From the anki-agent project directory
source /home/dangnd/code/github/anki-agent/.venv/bin/activate
anki-agent ping
```

If ping fails, instruct the user to:
1. Open Anki Desktop
2. Install AnkiConnect: `Tools → Add-ons → Get Add-ons... → 2055492159 → Restart`

## Command Reference

### Activating the CLI

Always activate the virtual environment first:

```bash
source /home/dangnd/code/github/anki-agent/.venv/bin/activate
```

### Connection & Status

```bash
anki-agent ping                    # Check connection
anki-agent version                 # AnkiConnect version
anki-agent sync                    # Sync with AnkiWeb
anki-agent profiles                # List profiles
```

### Deck Operations

```bash
anki-agent deck list               # List all decks (JSON: {decks, total})
anki-agent deck create "Name"      # Create deck
anki-agent deck delete "Name" --force  # Delete (REQUIRES --force)
anki-agent deck stats "Name"       # Deck statistics
anki-agent deck rename "Old" "New" # Rename deck
```

### Note Operations (Most Common)

```bash
# Discover available models and fields FIRST
anki-agent note models                    # List note types
anki-agent note model-fields "Basic"      # Show fields for a model

# Add a single note
anki-agent note add --deck "DeckName" --model "Basic" \
  --front "Question" --back "Answer" --tags tag1 tag2

# Add with custom fields (for non-Basic models like Cloze)
anki-agent note add --deck "DeckName" --model "Cloze" \
  --fields '{"Text": "{{c1::Paris}} is capital of France", "Extra": "info"}'

# Bulk add from JSON (stdin or file)
echo '[
  {"deck":"MyDeck","model":"Basic","fields":{"Front":"Q1","Back":"A1"},"tags":["ai"]},
  {"deck":"MyDeck","model":"Basic","fields":{"Front":"Q2","Back":"A2"},"tags":["ai"]}
]' | anki-agent note add-many --file -

# Search notes
anki-agent note find --query "deck:Default"           # By deck
anki-agent note find --query "tag:vocab" --details     # With full details
anki-agent note find --query "front:hello"             # By content
anki-agent note find --query "added:1"                 # Added today

# Get note details
anki-agent note info --ids 1234567890

# Update a note
anki-agent note update --id 1234567890 --field Front --value "New question"
anki-agent note update --id 1234567890 --fields '{"Front":"Q","Back":"A"}'

# Delete notes (REQUIRES --force)
anki-agent note delete --ids 1234567890 9876543210 --force
```

### Card Operations

```bash
anki-agent card find --query "is:due"          # Find due cards
anki-agent card find --query "is:new"          # Find new cards
anki-agent card due --deck "MyDeck" --limit 20 # Due cards with details
anki-agent card info --ids 100 200             # Card details
anki-agent card suspend --ids 100 200          # Suspend cards
anki-agent card unsuspend --ids 100            # Unsuspend
anki-agent card move --ids 100 --deck "Other"  # Move to another deck
```

### Tag Operations

```bash
anki-agent tag list                                    # List all tags
anki-agent tag add --notes 111 222 --tags "vocab new"  # Add tags
anki-agent tag remove --notes 111 --tags "old-tag"     # Remove tags
anki-agent tag find-notes vocab                        # Find notes by tag
anki-agent tag replace "old-tag" "new-tag"             # Replace tag globally
anki-agent tag clear --notes 111 --force               # Clear all tags
```

### Media Operations

```bash
anki-agent media store --filename "img.png" --path "/path/to/img.png"
anki-agent media store --filename "audio.mp3" --url "https://example.com/a.mp3"
anki-agent media list --pattern "*.png"
anki-agent media retrieve --filename "img.png" --output ./img.png
anki-agent media delete --filename "old.png" --force
```

## Workflows

### Deck Selection (Required First Step for All Workflows)

> [!IMPORTANT]
> **NEVER auto-create a deck.** Always fetch existing decks and let the user
> choose. Only create a new deck if the user explicitly requests it.

Every workflow that involves adding or moving cards **must** start with this
deck selection procedure:

1. **Fetch all existing decks**:
   ```bash
   anki-agent deck list
   ```
2. **Present the list** to the user as selectable options, e.g.:
   > Anki của bạn hiện có các decks sau:
   > 1. Default
   > 2. Japanese::Vocabulary
   > 3. Programming::Python
   >
   > Bạn muốn sử dụng deck nào, hoặc tạo deck mới?
3. **Wait for user selection**:
   - If user picks an existing deck → use that deck name
   - If user wants a new deck → ask for the name, then create:
     ```bash
     anki-agent deck create "UserChosenName"
     ```
4. Proceed to the next workflow step with the confirmed deck name.

### Workflow 1: Generate Flashcards from Text

When the user provides text (notes, article, conversation) and wants flashcards:

1. **Deck Selection** — follow the procedure above
2. **Check available models**: `anki-agent note models` then `anki-agent note model-fields "Basic"`
3. **Generate cards** from the content — create a JSON array of notes
4. **Bulk add**: pipe the JSON to `anki-agent note add-many --file -`
5. **Verify**: `anki-agent note find --query "tag:ai-generated added:1" --details`
6. **Report results** to the user

### Workflow 2: Review and Edit Existing Cards

1. **Deck Selection** — follow the procedure above to identify which deck to review
2. **Search**: `anki-agent note find --query "deck:DeckName" --details`
3. **Identify** cards to update from the JSON response
4. **Update**: `anki-agent note update --id <id> --field Front --value "corrected text"`
5. **Verify**: `anki-agent note info --ids <id>`

### Workflow 3: Organize Collection

1. **Deck Selection** — fetch decks and let user confirm scope
2. **List tags**: `anki-agent tag list`
3. **Find notes**: `anki-agent note find --query "<criteria>" --details`
4. **Re-tag**: `anki-agent tag add/remove --notes <ids> --tags "<tags>"`
5. **Move cards**: `anki-agent card move --ids <ids> --deck "TargetDeck"`
6. **Sync**: `anki-agent sync`

## Safety Rules

> [!CAUTION]
> - **NEVER** delete without `--force` flag AND explicit user confirmation
> - **ALWAYS** search/list before bulk operations to confirm scope
> - **ALWAYS** report what was done after destructive operations
> - **Tag AI-generated content** with `ai-generated` tag for traceability
> - **Sync after major changes**: run `anki-agent sync` after bulk operations

## Output Parsing

All commands output JSON. Key patterns:

```python
# Success response
{"status": "ok", "message": "...", "data": {...}}

# Data response
{"decks": [...], "total": 3}
{"note_ids": [111, 222], "total": 2}
{"notes": [{...}], "total": 1}

# Error response (stderr)
{"error": "error message"}
```

## Anki Search Query Syntax

Use these in `--query` parameters:

| Query | Meaning |
|---|---|
| `deck:DeckName` | Cards in a specific deck |
| `tag:tagname` | Notes with a tag |
| `front:text` | Front field contains text |
| `"front:exact phrase"` | Exact phrase match |
| `added:1` | Added today |
| `added:7` | Added in last 7 days |
| `is:due` | Cards due for review |
| `is:new` | New cards |
| `is:suspended` | Suspended cards |
| `rated:1` | Reviewed today |
| `-tag:exclude` | Notes WITHOUT a tag |
| `deck:A OR deck:B` | Multiple conditions |
