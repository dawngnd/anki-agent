---
name: english-learning
description: >-
  Creates English learning Anki flashcards from user-provided vocabulary,
  phrases, or conversation scripts. Automatically determines card type
  (vocabulary, phrase/cloze, situation-response) or asks the user.
  Handles deck selection, card generation with proper templates, and
  bulk insertion via anki-agent CLI. Use when the user wants to learn
  English vocabulary, conversational phrases, or situational expressions.
---

# English Learning Flashcard Skill

## Overview

This skill creates English learning flashcards for Vietnamese speakers. It
supports three card types optimized for different learning goals:

| Card Type | Goal | Anki Model | When to Use |
|-----------|------|------------|-------------|
| **Vocabulary** | Nhớ nghĩa, phát âm, cách dùng từ đơn | `Basic` | User provides word list or topic |
| **Phrase / Cloze** | Nhớ cách diễn đạt tự nhiên | `Cloze` | User provides phrases, dialogues, listening scripts |
| **Situation Response** | Phản xạ giao tiếp | `Basic` | User describes situations they want to practice |

## Prerequisites

- **anki-card-templates** skill — for base card formatting rules
- **anki-flashcard-management** skill — for CLI commands and deck workflow

> [!IMPORTANT]
> Always read and follow the `anki-flashcard-management` skill for CLI usage
> and the `anki-card-templates` skill for HTML formatting rules. This skill
> extends those with English-specific templates and workflow.

---

## Workflow

> [!IMPORTANT]
> **Core principle**: NEVER create Anki cards without user review first.
> The workflow is: Analyze → Research → **Review** → Create.

### Step 1: Analyze User Input

When the user provides content for English learning, classify it into one or
more of these categories:

| Input Type | Examples | → Card Type |
|-----------|----------|-------------|
| Word list | "learn: commute, resilient, ambiguous" | Vocabulary |
| Topic request | "cho tôi từ vựng về du lịch" | Vocabulary |
| Phrases / Sentences | "I haven't seen you in ages" | Phrase (Cloze) |
| Dialogue / Script | A conversation transcript | Phrase (Cloze) |
| Situation description | "cách hỏi đường lịch sự" | Situation Response |
| Mixed content | Article with new words + useful phrases | Vocabulary + Cloze |

### Step 2: Confirm Card Type with User

If the card type is ambiguous, ask the user:

> Bạn muốn tạo loại thẻ nào?
>
> 1. **Từ vựng** (Vocabulary) — Học từ đơn: nghĩa, phát âm, ví dụ
> 2. **Cụm từ / Mẫu câu** (Phrases) — Điền vào chỗ trống trong câu thực tế
> 3. **Phản xạ tình huống** (Situation) — Thấy tình huống → nhớ cách nói
> 4. **Kết hợp** — Tự động chọn loại phù hợp cho từng item

If the input clearly maps to one type (e.g., a list of single words → Vocabulary),
skip this step and proceed directly.

### Step 3: Research

> [!IMPORTANT]
> **Agent MUST research thoroughly before presenting to user.** Do NOT just
> generate content from memory. Use web search and reliable sources to verify
> accuracy of pronunciation, meanings, usage, and examples.

#### 3a. Research for Vocabulary

For each word, research and collect:

| Field | How to Research | Source Priority |
|-------|----------------|----------------|
| **IPA Pronunciation** | Search web for exact IPA | Cambridge Dictionary, Oxford Learner's |
| **Part of Speech** | Verify all relevant parts of speech | Dictionary sources |
| **Meaning(s)** | Primary meaning + important secondary meanings | Dictionary + context |
| **Collocations** | Common word combinations | Corpus-based dictionaries, OZDIC |
| **Example Sentence** | Natural, real-world usage | Dictionary examples or create realistic ones |
| **CEFR Level** | Frequency/difficulty assessment | English Profile, vocabulary lists |
| **Common Mistakes** | Errors Vietnamese speakers often make | Teaching resources |
| **Synonyms / Antonyms** | Related words for context | Thesaurus |

**Research procedure**:
1. Search `"{word}" definition pronunciation IPA` on the web
2. Verify IPA from Cambridge Dictionary or similar authoritative source
3. Check collocations and common usage patterns
4. For words with multiple meanings, identify which meanings are most useful
   for the learner's context (topic, level)

#### 3b. Research for Phrases

For each phrase/expression, research and collect:

| Field | How to Research | Source Priority |
|-------|----------------|----------------|
| **Exact Form** | Verify the standard/common form | Corpus search, dictionaries |
| **Meaning** | Precise Vietnamese translation | Bilingual resources |
| **Register** | Formal / Informal / Neutral | Usage notes in dictionaries |
| **Context** | When and where it's used | Example dialogues, forums |
| **Variations** | Common alternative phrasings | Native speaker resources |
| **Pronunciation Notes** | Connected speech, stress patterns | Listening resources |

**Research procedure**:
1. Search `"{phrase}" meaning usage examples` on the web
2. Verify the phrase is actually common and natural (not textbook-only)
3. Check if there are regional differences (US vs UK English)
4. Find real-world examples of usage

#### 3c. Research for Situation Responses

For each situation, research and collect:

| Field | How to Research |
|-------|----------------|
| **Most Natural Response** | What native speakers actually say |
| **Formality Variants** | Casual → Formal alternatives |
| **Cultural Notes** | Cross-cultural considerations |
| **Common Mistakes** | What non-native speakers incorrectly say |

### Step 4: Present Research for User Review

> [!IMPORTANT]
> **MUST present ALL research to the user in a clear, readable format BEFORE
> creating any Anki cards.** Wait for explicit user approval.

#### 4a. Vocabulary Review Format

Present as a numbered markdown table:

```markdown
## 📝 Kết quả nghiên cứu — Từ vựng [{topic}]

| # | Từ | Loại từ | Phát âm | Nghĩa | Ví dụ | Level |
|---|-----|---------|---------|-------|-------|-------|
| 1 | **commute** | verb/noun | /kəˈmjuːt/ | đi làm hàng ngày; quãng đường đi làm | _I **commute** to work by train._ | B1 |
| 2 | **resilient** | adj | /rɪˈzɪl.i.ənt/ | kiên cường, phục hồi nhanh | _Children are remarkably **resilient**._ | B2 |
| ... | | | | | | |

### Chi tiết bổ sung:

**1. commute**
- 🔗 Collocations: daily commute, long commute, commute to work
- ⚠️ Lưu ý: Người Việt hay nhầm với "communicate"
- 🔄 Synonyms: travel to work, make the journey

**2. resilient**
- 🔗 Collocations: resilient economy, emotionally resilient, remarkably resilient
- ⚠️ Lưu ý: Không dùng "resilient" cho đồ vật (dùng "durable" thay thế)
- 🔄 Synonyms: tough, hardy, adaptable

---
> Bạn muốn chỉnh sửa gì không? Có thể:
> - ❌ Bỏ từ nào không muốn học
> - ✏️ Sửa nghĩa / ví dụ
> - ➕ Thêm từ mới
> - ✅ OK — Tạo thẻ Anki
```

#### 4b. Phrase Review Format

```markdown
## 📝 Kết quả nghiên cứu — Cụm từ / Mẫu câu

| # | Phrase | Nghĩa | Dùng khi | Level |
|---|--------|-------|---------|-------|
| 1 | **long time no see** | Lâu rồi không gặp | Gặp lại bạn bè | A2 |
| 2 | **managed to squeeze in** | Cố xếp vào lịch | Kể về việc bận rộn | B2 |

### Chi tiết:

**1. long time no see**
- 📖 Register: Thân mật (informal)
- 💡 Variations: "It's been ages!", "I haven't seen you in forever!"
- 🗣️ Phát âm: Nhấn "long" và "see", nói liền
- ⚠️ Lưu ý: Chỉ dùng với người quen, không dùng trong email công việc

**2. managed to squeeze in**
- 📖 Register: Trung tính (neutral)
- 💡 Variations: "fit in", "make time for"
- 🗣️ Phát âm: /skwiːz ɪn/ — "squeeze" nhiều người Việt phát âm sai
- ⚠️ Lưu ý: "squeeze in" = chen vào (lịch trình), khác "squeeze" (bóp/nắn)

---
> Bạn muốn chỉnh sửa gì không?
> - ❌ Bỏ phrase nào không muốn học
> - ✏️ Sửa nghĩa / giải thích
> - ➕ Thêm phrase mới
> - ✅ OK — Tạo thẻ Anki
```

#### 4c. Situation Review Format

```markdown
## 📝 Kết quả nghiên cứu — Phản xạ tình huống [{context}]

| # | Tình huống | Cách nói tự nhiên | Level |
|---|-----------|-------------------|-------|
| 1 | Xin bàn cho 2 người | "Table for two, please." | A2 |
| 2 | Gọi món nhưng chưa quyết định | "Could you give us a few more minutes?" | A2 |

### Chi tiết:

**1. Xin bàn cho 2 người**
- ✨ Primary: "Hi, table for two, please."
- 🔄 Alternatives:
  - "Could we get a table for two?" (lịch sự hơn)
  - "We have a reservation under [name]." (nếu đã đặt)
- ⚠️ Tránh nói: "Give me a table" — quá thô lỗ
- 🌍 Văn hóa: Ở Mỹ thường có host/hostess đón ở cửa, đợi được dẫn vào

---
> Bạn muốn chỉnh sửa gì không?
> - ❌ Bỏ tình huống nào
> - ✏️ Sửa cách diễn đạt
> - ➕ Thêm tình huống mới
> - ✅ OK — Tạo thẻ Anki
```

### Step 5: Handle User Feedback

Based on user response to the review:

| User Action | Agent Response |
|-------------|---------------|
| ✅ "OK" / "Tạo đi" / "Được rồi" | Proceed to Step 6 (Deck Selection + Create) |
| ❌ "Bỏ từ 3, 5" | Remove those items, re-present updated list |
| ✏️ "Sửa nghĩa từ 2 thành ..." | Update the item, re-present updated list |
| ➕ "Thêm từ: elaborate" | Research the new word, add to list, re-present |
| 🔄 "Đổi ví dụ từ 1" | Generate new example, re-present |
| ❓ More info requested | Provide additional detail on the requested item |

> [!TIP]
> After any edit, re-present the **full updated list** so the user sees the
> final version. Only proceed to card creation when user explicitly approves.

### Step 6: Deck Selection

Follow the standard deck selection procedure from the `anki-flashcard-management`
skill:

1. Run `anki-agent deck list`
2. Present existing decks to user
3. Suggest the default structure if no English decks exist:
   - `English::Vocabulary` for vocabulary cards
   - `English::Phrases` for phrase and situation cards

> [!TIP]
> If the user already has English decks from previous sessions, reuse them.
> Only suggest creating new decks if none exist.

### Step 7: Generate & Insert Cards

Generate cards following the exact templates below. Then use `anki-agent note
add-many --file -` for bulk insertion.

Use the **reviewed and approved** content from Step 4-5 to populate the card
fields. Do NOT regenerate or change content — use exactly what the user approved.

### Step 8: Verify & Report

```bash
anki-agent note find --query "tag:ai-generated added:1" --details
anki-agent sync
```

Report to the user: number of cards created, deck, and card types used.

---

## Card Templates

### Template A: Vocabulary (Từ vựng)

**Model**: `Basic`
**Default Deck**: `English::Vocabulary`

**Front** — The English word with part of speech:
```html
<p style='font-size:1.5em'><strong>{word}</strong></p>
<p><em>{part_of_speech}</em></p>
```

**Back** — Pronunciation + Meaning + Example:
```html
<p><strong>Phát âm:</strong> /{ipa}/</p>
<p><strong>Nghĩa:</strong> {vietnamese_meaning}</p>
<hr>
<p><strong>Ví dụ:</strong></p>
<p><em>{example_sentence_with_<u>word</u>_underlined}</em></p>
<p>{vietnamese_translation_of_example}</p>
```

**Required tags**: `type::vocab`, `level::{cefr_level}`, `topic::{topic}`

**Complete JSON example**:
```json
{
  "deck": "English::Vocabulary",
  "model": "Basic",
  "fields": {
    "Front": "<p style='font-size:1.5em'><strong>commute</strong></p><p><em>verb / noun</em></p>",
    "Back": "<p><strong>Phát âm:</strong> /kəˈmjuːt/</p><p><strong>Nghĩa:</strong> (v) đi làm hàng ngày; (n) quãng đường đi làm</p><hr><p><strong>Ví dụ:</strong></p><p><em>I <u>commute</u> to the office by subway every day.</em></p><p>Tôi đi làm bằng tàu điện ngầm mỗi ngày.</p>"
  },
  "tags": ["type::vocab", "topic::daily-life", "topic::work", "level::B1", "ai-generated"]
}
```

**Rules for Vocabulary cards**:
1. **One primary meaning per card** — if a word has multiple important meanings, create multiple cards
2. **Always include an example sentence** — context aids retention
3. **Underline the target word** in the example with `<u>` tags
4. **Include IPA pronunciation** — look up correct phonetic transcription
5. **Tag by CEFR level** — `level::A2`, `level::B1`, `level::B2`, etc.
6. **Tag by topic** — `topic::travel`, `topic::food`, `topic::work`, etc.

---

### Template B: Phrase / Cloze (Cụm từ / Mẫu câu)

**Model**: `Cloze`
**Default Deck**: `English::Phrases`

**Text** — Sentence with cloze deletion on the key phrase:
```html
<p><strong>{emoji} {situation_label}</strong></p>
<p>{sentence_with_{{c1::key_phrase}}_cloze}</p>
```

**Extra** — Vietnamese meaning + usage note:
```html
<p><strong>Nghĩa:</strong> {vietnamese_translation}</p>
<p><strong>Dùng khi:</strong> {when_to_use}</p>
```

**Required tags**: `type::phrase`, `situation::{situation}`, `level::{cefr_level}`

**Complete JSON example**:
```json
{
  "deck": "English::Phrases",
  "model": "Cloze",
  "fields": {
    "Text": "<p><strong>🎧 Greeting</strong></p><p>{{c1::I haven't seen you}} in ages! How have you been?</p>",
    "Extra": "<p><strong>Nghĩa:</strong> Lâu lắm rồi không gặp! Dạo này bạn thế nào?</p><p><strong>Dùng khi:</strong> Gặp lại bạn bè sau thời gian dài</p>"
  },
  "tags": ["type::phrase", "situation::greeting", "level::B1", "ai-generated"]
}
```

**Rules for Phrase/Cloze cards**:
1. **Cloze the key phrase**, not random words — the cloze should be the part the learner needs to recall
2. **Use emoji + label** for situation context at the top: 🎧 Greeting, 🍽️ Ordering, 💭 Opinion, etc.
3. **Keep surrounding context** meaningful — don't cloze so much the sentence is unrecognizable
4. **Use separate cloze numbers** (`c1`, `c2`) only when testing separate facts
5. **Add hint** with `{{c1::answer::hint}}` if the cloze is ambiguous
6. **Extra field** must include Vietnamese translation and usage context
7. **For dialogues**: extract the most useful/natural phrases, not every line

**Choosing what to cloze**:
- ✅ Idiomatic expressions: `{{c1::I haven't seen you}} in ages`
- ✅ Collocations: `Could I {{c1::get}} the chicken salad`
- ✅ Discourse markers: `{{c1::As far as I'm concerned}}, we should...`
- ✅ Phrasal verbs: `The meeting was {{c1::called off}} due to rain`
- ❌ Don't cloze common words like "the", "is", "a"
- ❌ Don't cloze proper nouns or numbers

---

### Template C: Situation Response (Phản xạ tình huống)

**Model**: `Basic`
**Default Deck**: `English::Phrases`

**Front** — Situation described in Vietnamese:
```html
<p><strong>🎭 Situation:</strong></p>
<p>{situation_description_in_vietnamese}</p>
<p><em>Nói bằng tiếng Anh?</em></p>
```

**Back** — Natural English response + alternatives:
```html
<p><strong>Cách nói tự nhiên:</strong></p>
<p style='font-size:1.2em'><em>"{primary_response}"</em></p>
<hr>
<p><strong>Các cách khác:</strong></p>
<ul>
  <li>"{alternative_1}"</li>
  <li>"{alternative_2}"</li>
</ul>
<p><strong>Lưu ý:</strong> {usage_note}</p>
```

**Required tags**: `type::situation`, `situation::{situation}`, `level::{cefr_level}`

**Complete JSON example**:
```json
{
  "deck": "English::Phrases",
  "model": "Basic",
  "fields": {
    "Front": "<p><strong>🎭 Situation:</strong></p><p>Bạn muốn <strong>hỏi đường</strong> đến nhà ga gần nhất một cách lịch sự.</p><p><em>Nói bằng tiếng Anh?</em></p>",
    "Back": "<p><strong>Cách nói tự nhiên:</strong></p><p style='font-size:1.2em'><em>\"Excuse me, could you tell me how to get to the nearest train station?\"</em></p><hr><p><strong>Các cách khác:</strong></p><ul><li>\"Do you happen to know where the train station is?\"</li><li>\"I'm looking for the train station. Could you point me in the right direction?\"</li></ul><p><strong>Lưu ý:</strong> Bắt đầu bằng 'Excuse me' để lịch sự. 'Could you tell me...' trang trọng hơn 'Where is...'</p>"
  },
  "tags": ["type::situation", "situation::asking-directions", "level::A2", "ai-generated"]
}
```

**Rules for Situation Response cards**:
1. **Front in Vietnamese** — describe the situation the learner would face
2. **Bold the key action** in the situation: "Bạn muốn **hỏi đường**..."
3. **Primary response** should be the most natural, commonly used expression
4. **Provide 2-3 alternatives** at different formality levels
5. **Add usage notes** — explain when each variation is appropriate
6. **Tag by situation** — `situation::greeting`, `situation::ordering`, etc.

---

## Tag System

Always apply these tags to generated cards:

| Tag Prefix | Purpose | Examples |
|-----------|---------|---------|
| `type::` | Card type | `type::vocab`, `type::phrase`, `type::situation` |
| `topic::` | Vocabulary topic | `topic::travel`, `topic::food`, `topic::work`, `topic::health` |
| `situation::` | Conversation context | `situation::greeting`, `situation::ordering`, `situation::small-talk` |
| `level::` | CEFR level | `level::A1`, `level::A2`, `level::B1`, `level::B2`, `level::C1` |
| `source::` | Content source | `source::podcast`, `source::movie`, `source::textbook`, `source::conversation` |
| `ai-generated` | Traceability | Always add this tag |

---

## Common Situation Labels (Emoji Reference)

Use these emoji + label combinations consistently in Phrase/Cloze cards:

| Emoji | Label | Dùng cho |
|-------|-------|---------|
| 🎧 | Greeting | Chào hỏi |
| 💬 | Small Talk | Nói chuyện phiếm |
| 🍽️ | Ordering | Gọi món, mua hàng |
| 🗺️ | Directions | Hỏi/chỉ đường |
| 💭 | Opinion | Bày tỏ ý kiến |
| 🤝 | Request | Nhờ vả, yêu cầu |
| 📞 | Phone | Nói chuyện điện thoại |
| 🏥 | Health | Sức khỏe, khám bệnh |
| 🏨 | Hotel | Đặt phòng, check-in |
| ✈️ | Travel | Sân bay, di chuyển |
| 💼 | Work | Công việc, họp hành |
| 😊 | Compliment | Khen ngợi |
| 😢 | Sympathy | Chia buồn, đồng cảm |
| 🎉 | Congratulations | Chúc mừng |
| ❌ | Declining | Từ chối lịch sự |
| 🙏 | Apologizing | Xin lỗi |

---

## Bulk Generation Format

When generating multiple cards, output a single JSON array and pipe to CLI:

```bash
cat <<'EOF' | anki-agent note add-many --file -
[
  { "deck": "...", "model": "...", "fields": {...}, "tags": [...] },
  { "deck": "...", "model": "...", "fields": {...}, "tags": [...] }
]
EOF
```

> [!CAUTION]
> - Always validate JSON before piping to `add-many`
> - Always tag with `ai-generated` for traceability
> - Verify after adding: `anki-agent note find --query "tag:ai-generated added:1" --details`
> - Sync after major additions: `anki-agent sync`
