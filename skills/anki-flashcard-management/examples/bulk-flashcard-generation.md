# Example: Bulk Flashcard Generation

## Input Text

> Photosynthesis is the process by which green plants convert sunlight, water,
> and carbon dioxide into glucose and oxygen. It occurs in the chloroplasts,
> specifically in the thylakoid membranes. The process has two stages:
> light-dependent reactions and the Calvin cycle.

## Generated JSON for `anki-agent note add-many`

```json
[
  {
    "deck": "Biology::Photosynthesis",
    "model": "Basic",
    "fields": {
      "Front": "What is photosynthesis?",
      "Back": "The process by which green plants convert sunlight, water, and CO₂ into glucose and oxygen."
    },
    "tags": ["biology", "photosynthesis", "ai-generated"]
  },
  {
    "deck": "Biology::Photosynthesis",
    "model": "Basic",
    "fields": {
      "Front": "Where does photosynthesis occur in the cell?",
      "Back": "In the chloroplasts, specifically in the thylakoid membranes."
    },
    "tags": ["biology", "photosynthesis", "ai-generated"]
  },
  {
    "deck": "Biology::Photosynthesis",
    "model": "Basic",
    "fields": {
      "Front": "What are the two stages of photosynthesis?",
      "Back": "1. Light-dependent reactions\n2. The Calvin cycle (light-independent reactions)"
    },
    "tags": ["biology", "photosynthesis", "ai-generated"]
  },
  {
    "deck": "Biology::Photosynthesis",
    "model": "Cloze",
    "fields": {
      "Text": "Photosynthesis converts {{c1::sunlight}}, {{c2::water}}, and {{c3::CO₂}} into {{c4::glucose}} and {{c5::oxygen}}.",
      "Extra": "Basic equation: 6CO₂ + 6H₂O + light → C₆H₁₂O₆ + 6O₂"
    },
    "tags": ["biology", "photosynthesis", "ai-generated", "cloze"]
  }
]
```

## Commands to Execute

```bash
# 1. Create deck
anki-agent deck create "Biology::Photosynthesis"

# 2. Add all cards (pipe JSON via stdin)
cat <<'EOF' | anki-agent note add-many --file -
[
  {"deck":"Biology::Photosynthesis","model":"Basic","fields":{"Front":"What is photosynthesis?","Back":"The process by which green plants convert sunlight, water, and CO₂ into glucose and oxygen."},"tags":["biology","photosynthesis","ai-generated"]},
  {"deck":"Biology::Photosynthesis","model":"Basic","fields":{"Front":"Where does photosynthesis occur?","Back":"In the chloroplasts, specifically in the thylakoid membranes."},"tags":["biology","photosynthesis","ai-generated"]},
  {"deck":"Biology::Photosynthesis","model":"Basic","fields":{"Front":"What are the two stages of photosynthesis?","Back":"1. Light-dependent reactions\n2. The Calvin cycle"},"tags":["biology","photosynthesis","ai-generated"]}
]
EOF

# 3. Verify
anki-agent note find --query "tag:ai-generated added:1" --details

# 4. Sync
anki-agent sync
```
