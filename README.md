# anki-agent

CLI tools for AI Agents to manage Anki flashcards via [AnkiConnect](https://git.sr.ht/~foosoft/anki-connect).

## Prerequisites

1. **Anki Desktop** (v2.1.x+ / v26.x) — [Download](https://apps.ankiweb.net/)
2. **AnkiConnect add-on** — Install via Anki:
   - `Tools → Add-ons → Get Add-ons...` → Code: `2055492159` → Restart Anki

Verify AnkiConnect is running:

```bash
curl localhost:8765 -X POST -d '{"action":"version","version":6}'
# Expected: {"result":6,"error":null}
```

## Installation

```bash
# Install uv (nếu chưa có)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Tạo virtual environment và cài đặt
uv venv .venv
source .venv/bin/activate
uv pip install -e .

# Verify
anki-agent --version
anki-agent ping
```

## Configuration

| Environment Variable | Description | Default |
|---|---|---|
| `ANKI_CONNECT_URL` | AnkiConnect server URL | `http://localhost:8765` |
| `ANKI_CONNECT_API_KEY` | API key for authentication | _(none)_ |

Or use CLI flags: `--url`, `--api-key`

## Usage

All commands output **JSON** for easy parsing by AI agents.

### Connection

```bash
anki-agent ping                    # Check connection
anki-agent version                 # AnkiConnect version
anki-agent sync                    # Sync with AnkiWeb
anki-agent profiles                # List profiles
```

### Deck Management

```bash
anki-agent deck list                              # List all decks
anki-agent deck create "Japanese::Vocabulary"      # Create (:: for nested)
anki-agent deck delete "Old Deck" --force          # Delete (requires --force)
anki-agent deck stats "Default"                    # Statistics
anki-agent deck rename "Old Name" "New Name"       # Rename
```

### Note Management

```bash
anki-agent note models                             # List note types
anki-agent note model-fields "Basic"               # Show fields for a model

# Add a note
anki-agent note add --deck "Default" --model "Basic" --front "Hello" --back "Xin chào"

# Add with custom fields (for non-Basic models)
anki-agent note add --deck "Default" --model "Cloze" \
  --fields '{"Text": "{{c1::Paris}} is the capital of France", "Extra": "Geography"}'

# Add with tags
anki-agent note add --deck "Default" --front "Q" --back "A" --tags vocab important

# Bulk add from JSON file or stdin
anki-agent note add-many --file notes.json
echo '[{"deck":"Default","model":"Basic","fields":{"Front":"Q","Back":"A"}}]' | anki-agent note add-many --file -

# Search, view, update, delete
anki-agent note find --query "deck:Default"
anki-agent note find --query "tag:vocab" --details
anki-agent note info --ids 1234567890
anki-agent note update --id 1234567890 --field Front --value "Updated"
anki-agent note delete --ids 1234567890 --force
```

### Card Management

```bash
anki-agent card find --query "is:due"              # Find cards
anki-agent card info --ids 100 200                 # Card details
anki-agent card due --deck "Japanese" --limit 50   # Due for review
anki-agent card suspend --ids 100 200              # Suspend
anki-agent card unsuspend --ids 100                # Unsuspend
anki-agent card move --ids 100 --deck "Archive"    # Move to deck
```

### Tag Management

```bash
anki-agent tag list                                        # All tags
anki-agent tag add --notes 111 222 --tags "vocab important" # Add
anki-agent tag remove --notes 111 --tags "old-tag"          # Remove
anki-agent tag find-notes vocab                             # Find by tag
anki-agent tag replace "old-tag" "new-tag"                  # Replace
anki-agent tag clear --notes 111 --force                    # Clear all
```

### Media Management

```bash
anki-agent media store --filename "img.png" --path "/path/to/img.png"
anki-agent media store --filename "audio.mp3" --url "https://example.com/a.mp3"
anki-agent media list --pattern "*.png"
anki-agent media retrieve --filename "img.png" --output ./img.png
anki-agent media delete --filename "old.png" --force
```

## JSON Input Format for Bulk Notes

```json
[
  {
    "deck": "Japanese::Vocabulary",
    "model": "Basic",
    "fields": { "Front": "猫", "Back": "cat" },
    "tags": ["japanese", "n5"]
  },
  {
    "deck": "Japanese::Vocabulary",
    "model": "Basic",
    "fields": { "Front": "犬", "Back": "dog" },
    "tags": ["japanese", "n5"]
  }
]
```

---

## AI Agent Skills

Project này đi kèm **2 agent skills** trong `.agents/skills/`, được AI agents (Antigravity, Claude, Cursor...) tự động phát hiện khi làm việc trong workspace.

### Cấu trúc Skills

```
.agents/skills/
├── anki-flashcard-management/          # Skill 1: Quản lý CLI
│   ├── SKILL.md                        # Hướng dẫn chạy anki-agent CLI
│   ├── scripts/setup.sh                # Script kiểm tra kết nối
│   └── examples/
│       ├── bulk-flashcard-generation.md # Ví dụ tạo hàng loạt
│       └── vietnamese-vocabulary.md     # Ví dụ tiếng Việt
│
└── anki-card-templates/                # Skill 2: Thiết kế nội dung thẻ
    ├── SKILL.md                        # 7 templates + quy tắc format
    └── examples/
        └── mixed-templates.md          # Ví dụ kết hợp templates
```

### Skill 1: `anki-flashcard-management`

Hướng dẫn agent cách sử dụng `anki-agent` CLI — kết nối, CRUD decks/notes/cards/tags/media.

**Quy trình bắt buộc:**
1. Kiểm tra kết nối (`anki-agent ping`)
2. **Fetch danh sách decks** → hỏi user chọn deck hoặc tạo mới (không tự tạo)
3. Thực hiện thao tác
4. Verify kết quả
5. Sync nếu cần

### Skill 2: `anki-card-templates`

Định nghĩa **7 templates** để agent format nội dung thẻ chất lượng cao:

| # | Template | Model | Dùng cho |
|---|---|---|---|
| 1 | **Basic Q&A** | Basic | Kiến thức đơn giản, câu hỏi trả lời |
| 2 | **Vocabulary** | Basic | Từ vựng (từ, phiên âm, nghĩa, ví dụ) |
| 3 | **Cloze Deletion** | Cloze | Điền vào chỗ trống trong ngữ cảnh |
| 4 | **Code** | Basic | Code snippets, lập trình |
| 5 | **Concept Definition** | Basic | Khái niệm, định nghĩa học thuật |
| 6 | **Comparison** | Basic | So sánh X vs Y (bảng HTML) |
| 7 | **Process / Steps** | Basic | Quy trình, thuật toán, các bước |

**Quy trình bắt buộc:**
1. Agent hỏi user chọn template
2. Agent hỏi user chọn deck
3. Tạo nội dung theo template đã chọn (HTML formatting)
4. Thêm vào Anki và verify

### Cài đặt Skills cho AI Agent

#### Cách 1: Tự động (Workspace-level) — Khuyến nghị

Skills đã nằm sẵn trong `.agents/skills/`. Bất kỳ AI agent tương thích nào mở workspace này đều **tự động phát hiện** và sử dụng skills.

```bash
# Không cần cài gì thêm — chỉ cần mở project trong agent
cd /path/to/anki-agent
# Agent sẽ tự thấy skills trong .agents/skills/
```

#### Cách 2: Copy vào Global Config (dùng cho mọi project)

Nếu muốn skills khả dụng ở **tất cả workspaces**:

```bash
# Antigravity / AGY
cp -r .agents/skills/anki-flashcard-management ~/.gemini/config/skills/
cp -r .agents/skills/anki-card-templates ~/.gemini/config/skills/
```

#### Cách 3: Symlink từ project khác

Dùng skills từ workspace khác mà không duplicate:

```bash
# Trong project khác, tạo symlink
mkdir -p /path/to/other-project/.agents/skills
ln -s /path/to/anki-agent/.agents/skills/anki-flashcard-management \
      /path/to/other-project/.agents/skills/anki-flashcard-management
ln -s /path/to/anki-agent/.agents/skills/anki-card-templates \
      /path/to/other-project/.agents/skills/anki-card-templates
```

### Sử dụng Skills

Sau khi cài đặt, chỉ cần nói với AI agent bằng ngôn ngữ tự nhiên:

```
🗣 "Tạo 10 thẻ flashcard về Python decorators"
🗣 "Tạo thẻ từ vựng tiếng Nhật N5 về ẩm thực"
🗣 "Tìm tất cả thẻ có tag 'grammar' và chuyển sang deck mới"
🗣 "Tóm tắt bài viết này thành flashcards dạng cloze"
🗣 "So sánh REST vs GraphQL, tạo thẻ comparison"
```

Agent sẽ tự động:
1. Kích hoạt skill phù hợp
2. Hỏi bạn chọn **template** (Basic Q&A, Vocabulary, Cloze, Code...)
3. Hỏi bạn chọn **deck** (hiện danh sách decks có sẵn)
4. Tạo thẻ theo template đã chọn
5. Thêm vào Anki và xác nhận kết quả

### Ví dụ luồng hoạt động

```
User: "Tạo flashcard về Docker containers"

Agent: Bạn muốn dùng template nào?
  1. Basic Q&A
  2. Cloze Deletion
  3. Code
  4. Concept Definition
  ...

User: chọn 4 (Concept) và 3 (Code)

Agent: Anki của bạn hiện có các decks:
  1. Default
  2. Programming::Python
  3. DevOps
  Bạn muốn dùng deck nào, hoặc tạo mới?

User: Tạo mới "DevOps::Docker"

Agent: ✅ Đã tạo deck "DevOps::Docker"
       ✅ Đã thêm 8 thẻ flashcard (5 Concept + 3 Code)
       ✅ Đã sync với AnkiWeb
```

---

## Development

```bash
# Activate venv
source .venv/bin/activate

# Run tests
python -m pytest tests/ -v

# Run a specific test
python -m pytest tests/test_client.py -v
```

## License

MIT
