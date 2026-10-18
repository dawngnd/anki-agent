# Walkthrough: Anki Agent CLI Tools

## Tổng kết công việc

### Đã hoàn thành

Xây dựng hoàn chỉnh bộ **Python CLI tools** (`anki-agent`) cho AI Agent quản lý thẻ Anki thông qua AnkiConnect API.

### Files đã tạo (16 files)

| File | Mô tả |
|---|---|
| `pyproject.toml` | Project config, zero dependencies |
| `README.md` | Hướng dẫn sử dụng đầy đủ |
| `src/anki_agent/__init__.py` | Package init |
| `src/anki_agent/client.py` | AnkiConnect HTTP client (core) |
| `src/anki_agent/cli.py` | CLI entry point (argparse) |
| `src/anki_agent/utils.py` | Output helpers |
| `src/anki_agent/commands/__init__.py` | Commands package |
| `src/anki_agent/commands/deck.py` | Deck commands (5 subcommands) |
| `src/anki_agent/commands/note.py` | Note commands (10 subcommands) |
| `src/anki_agent/commands/card.py` | Card commands (6 subcommands) |
| `src/anki_agent/commands/tag.py` | Tag commands (6 subcommands) |
| `src/anki_agent/commands/media.py` | Media commands (4 subcommands) |
| `tests/__init__.py` | Tests package |
| `tests/test_client.py` | Client unit tests (10 tests) |
| `tests/test_commands.py` | CLI integration tests (21 tests) |

### Tính năng chính

- **35+ subcommands** trải đều 5 nhóm: deck, note, card, tag, media
- **JSON output** — tất cả output đều là JSON, dễ parse cho AI agent
- **Zero dependencies** — chỉ dùng Python stdlib
- **API key support** — qua `--api-key` flag hoặc env `ANKI_CONNECT_API_KEY`
- **Safety guards** — lệnh delete/clear yêu cầu `--force`
- **Sync command** — trigger sync với AnkiWeb
- **Bulk import** — thêm nhiều notes từ JSON file hoặc stdin

### Test Results

```
Ran 31 tests in 0.119s — OK
```

Tất cả 31 tests pass (mocked, không cần Anki chạy).

### Hướng dẫn sử dụng

1. Cài AnkiConnect add-on: `Tools → Add-ons → Get Add-ons → 2055492159`
2. Chạy: `PYTHONPATH=src python3 -m anki_agent.cli ping`
3. Hoặc cài vào hệ thống: `pip install -e .` → `anki-agent ping`
