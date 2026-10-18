# Example: Vietnamese Language Flashcards

## Scenario
User says: "Tạo cho tôi 5 thẻ từ vựng tiếng Việt chủ đề ẩm thực"

## Agent Execution

```bash
# 1. Check connection
anki-agent ping

# 2. Create deck
anki-agent deck create "Vietnamese::Ẩm thực"

# 3. Check model fields
anki-agent note model-fields "Basic"

# 4. Add cards
cat <<'EOF' | anki-agent note add-many --file -
[
  {
    "deck": "Vietnamese::Ẩm thực",
    "model": "Basic",
    "fields": {
      "Front": "phở",
      "Back": "Vietnamese noodle soup, typically made with beef or chicken broth, rice noodles, herbs, and meat"
    },
    "tags": ["vietnamese", "food", "ai-generated"]
  },
  {
    "deck": "Vietnamese::Ẩm thực",
    "model": "Basic",
    "fields": {
      "Front": "bánh mì",
      "Back": "Vietnamese baguette sandwich filled with various meats, pickled vegetables, cilantro, and chili"
    },
    "tags": ["vietnamese", "food", "ai-generated"]
  },
  {
    "deck": "Vietnamese::Ẩm thực",
    "model": "Basic",
    "fields": {
      "Front": "bún chả",
      "Back": "Grilled pork with rice noodles, herbs, and dipping sauce — a signature dish of Hanoi"
    },
    "tags": ["vietnamese", "food", "ai-generated"]
  },
  {
    "deck": "Vietnamese::Ẩm thực",
    "model": "Basic",
    "fields": {
      "Front": "gỏi cuốn",
      "Back": "Fresh spring rolls wrapped in rice paper with shrimp, pork, herbs, and rice vermicelli"
    },
    "tags": ["vietnamese", "food", "ai-generated"]
  },
  {
    "deck": "Vietnamese::Ẩm thực",
    "model": "Basic",
    "fields": {
      "Front": "cà phê sữa đá",
      "Back": "Vietnamese iced coffee with condensed milk — strong dark roast coffee dripped through a phin filter"
    },
    "tags": ["vietnamese", "food", "drink", "ai-generated"]
  }
]
EOF

# 5. Verify
anki-agent note find --query "deck:Vietnamese::Ẩm thực" --details

# 6. Sync
anki-agent sync
```
