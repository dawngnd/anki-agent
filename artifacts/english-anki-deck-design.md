# 🎯 Thiết kế Anki Deck cho Học Tiếng Anh

## Tổng quan

Bạn có **2 nhu cầu học** khác nhau, và mỗi nhu cầu cần cách thiết kế deck + template khác nhau:

| Nhu cầu | Mục tiêu | Template phù hợp |
|---------|----------|-------------------|
| **Từ vựng theo chủ đề** | Nhớ nghĩa, phát âm, cách dùng của từ đơn lẻ | Vocabulary (Basic) |
| **Phrase / Câu template** | Nhớ cách diễn đạt tự nhiên trong hội thoại | Cloze Deletion + Basic Q&A |

---

## 📂 Cấu trúc Deck đề xuất

```
English
├── English::Vocabulary
│   ├── (tag: topic::travel)
│   ├── (tag: topic::work)
│   ├── (tag: topic::health)
│   ├── (tag: topic::food)
│   └── (tag: topic::daily-life)
└── English::Phrases
    ├── (tag: situation::greeting)
    ├── (tag: situation::small-talk)
    ├── (tag: situation::ordering)
    ├── (tag: situation::asking-directions)
    └── (tag: situation::opinion)
```

> [!TIP]
> **Dùng 1 parent deck `English` với 2 sub-deck** thay vì tạo nhiều deck rời rạc. Dùng **tags** để phân loại theo chủ đề/tình huống — linh hoạt hơn nhiều so với tạo nhiều deck.

### Tại sao dùng Tag thay vì tạo nhiều Deck?

- ✅ Anki xử lý scheduling tốt hơn khi ít deck
- ✅ Dễ dàng tìm kiếm & lọc bằng Custom Study / Filtered Deck
- ✅ Một thẻ có thể thuộc nhiều chủ đề (1 từ vừa liên quan `food` vừa `travel`)
- ✅ Không bị phân tán review queue

---

## 🔤 Template 1: Từ vựng đơn lẻ (Vocabulary)

**Model**: `Basic` | **Deck**: `English::Vocabulary`

### Thiết kế thẻ

**Mặt trước (Front)** — Hiển thị từ tiếng Anh:
```html
<p style='font-size:1.5em'><strong>resilient</strong></p>
<p><em>adjective</em></p>
```

**Mặt sau (Back)** — Phát âm + Nghĩa + Ví dụ:
```html
<p><strong>Phát âm:</strong> /rɪˈzɪl.i.ənt/</p>
<p><strong>Nghĩa:</strong> kiên cường, có khả năng phục hồi nhanh</p>
<hr>
<p><strong>Ví dụ:</strong></p>
<p><em>Children are remarkably <u>resilient</u> — they bounce back quickly from setbacks.</em></p>
<p>Trẻ em rất kiên cường — chúng phục hồi nhanh chóng sau những thất bại.</p>
```

### Ví dụ JSON hoàn chỉnh

```json
{
  "deck": "English::Vocabulary",
  "model": "Basic",
  "fields": {
    "Front": "<p style='font-size:1.5em'><strong>commute</strong></p><p><em>verb / noun</em></p>",
    "Back": "<p><strong>Phát âm:</strong> /kəˈmjuːt/</p><p><strong>Nghĩa:</strong> (v) đi làm hàng ngày; (n) quãng đường đi làm</p><hr><p><strong>Ví dụ:</strong></p><p><em>I <u>commute</u> to the office by subway every day.</em></p><p>Tôi đi làm bằng tàu điện ngầm mỗi ngày.</p>"
  },
  "tags": ["topic::daily-life", "topic::work", "level::B1"]
}
```

### Quy tắc cho Vocabulary cards

1. **1 nghĩa chính per card** — nếu từ có nhiều nghĩa quan trọng, tạo nhiều thẻ
2. **Luôn có câu ví dụ** — giúp nhớ ngữ cảnh, không chỉ nhớ nghĩa
3. **Gạch chân từ trong ví dụ** — dễ nhận ra từ đang học
4. **Thêm phiên âm IPA** — giúp phát âm đúng
5. **Tag theo level** — `level::A2`, `level::B1`, `level::B2`...

---

## 💬 Template 2: Phrases & Câu template hội thoại

Đây là phần quan trọng nhất cho giao tiếp. Tôi đề xuất **kết hợp 2 loại thẻ**:

### Loại 2a: Cloze Deletion — Điền vào chỗ trống

**Model**: `Cloze` | **Deck**: `English::Phrases`

> [!IMPORTANT]
> **Cloze là template tốt nhất cho phrases** vì nó buộc bạn phải nhớ từ/cụm từ trong ngữ cảnh thực tế, thay vì chỉ nhận ra nghĩa.

**Ví dụ 1 — Greeting:**
```json
{
  "deck": "English::Phrases",
  "model": "Cloze",
  "fields": {
    "Text": "<p><strong>🎧 Greeting</strong></p><p>{{c1::I haven't seen you}} in ages! How have you been?</p>",
    "Extra": "<p><strong>Nghĩa:</strong> Lâu lắm rồi không gặp! Dạo này bạn thế nào?</p><p><strong>Dùng khi:</strong> Gặp lại bạn bè sau thời gian dài</p>"
  },
  "tags": ["situation::greeting", "source::podcast", "level::B1"]
}
```

**Ví dụ 2 — Ordering food:**
```json
{
  "deck": "English::Phrases",
  "model": "Cloze",
  "fields": {
    "Text": "<p><strong>🍽️ Ordering</strong></p><p>Could I {{c1::get}} the chicken salad, and {{c2::I'll have}} a sparkling water, please?</p>",
    "Extra": "<p><strong>Nghĩa:</strong> Cho tôi món salad gà, và tôi sẽ uống nước có ga.</p><p><strong>Lưu ý:</strong> 'Could I get...' tự nhiên hơn 'I want...'</p>"
  },
  "tags": ["situation::ordering", "source::listening", "level::A2"]
}
```

**Ví dụ 3 — Expressing opinion:**
```json
{
  "deck": "English::Phrases",
  "model": "Cloze",
  "fields": {
    "Text": "<p><strong>💭 Opinion</strong></p><p>{{c1::As far as I'm concerned}}, we should focus on quality over quantity.</p>",
    "Extra": "<p><strong>Nghĩa:</strong> Theo quan điểm của tôi, chúng ta nên tập trung vào chất lượng hơn số lượng.</p><p><strong>Tương đương:</strong> In my opinion / From my perspective</p>"
  },
  "tags": ["situation::opinion", "source::podcast", "level::B2"]
}
```

### Loại 2b: Basic Q&A — Tình huống → Phản xạ

**Model**: `Basic` | **Deck**: `English::Phrases`

> Dùng khi bạn muốn luyện **phản xạ**: thấy tình huống → nhớ ra cách nói.

**Ví dụ:**
```json
{
  "deck": "English::Phrases",
  "model": "Basic",
  "fields": {
    "Front": "<p><strong>🎭 Situation:</strong></p><p>Bạn muốn <strong>hỏi đường</strong> đến nhà ga gần nhất một cách lịch sự.</p><p><em>Nói bằng tiếng Anh?</em></p>",
    "Back": "<p><strong>Cách nói tự nhiên:</strong></p><p style='font-size:1.2em'><em>\"Excuse me, could you tell me how to get to the nearest train station?\"</em></p><hr><p><strong>Các cách khác:</strong></p><ul><li>\"Do you happen to know where the train station is?\"</li><li>\"I'm looking for the train station. Could you point me in the right direction?\"</li></ul>"
  },
  "tags": ["situation::asking-directions", "type::situation-response", "level::A2"]
}
```

---

## 🏷️ Hệ thống Tag đề xuất

| Prefix | Mục đích | Ví dụ |
|--------|---------|-------|
| `topic::` | Chủ đề từ vựng | `topic::travel`, `topic::food`, `topic::work` |
| `situation::` | Tình huống hội thoại | `situation::greeting`, `situation::ordering` |
| `level::` | Trình độ CEFR | `level::A2`, `level::B1`, `level::B2` |
| `source::` | Nguồn bài học | `source::podcast`, `source::movie`, `source::textbook` |
| `type::` | Loại thẻ | `type::vocab`, `type::phrase`, `type::situation-response` |

---

## 🎯 Khuyến nghị: Nên học cả 2!

> [!IMPORTANT]
> **Đừng chọn 1 trong 2 — hãy kết hợp cả hai**, nhưng với tỷ lệ phù hợp:

### Tỷ lệ đề xuất

```
┌─────────────────────────────────────────┐
│         Phân bổ thẻ mới / ngày          │
│                                         │
│   Vocabulary: 30-40%  ████████░░░░░░░░  │
│   Phrases:    60-70%  █████████████░░░  │
│                                         │
└─────────────────────────────────────────┘
```

### Lý do ưu tiên Phrases hơn:

1. **Từ vựng đơn lẻ dễ quên** — không có ngữ cảnh để gắn kết
2. **Phrases giúp giao tiếp ngay** — bạn có "sẵn câu" để dùng
3. **Học phrase = học vocabulary** — trong 1 phrase chứa nhiều từ mới
4. **Tự nhiên hơn** — người bản xứ nói theo cụm, không theo từ đơn

### Chiến lược học hiệu quả

| Bước | Hành động |
|------|-----------|
| 1 | Nghe bài hội thoại (podcast, video, phim) |
| 2 | Ghi lại các phrase hay, câu template thú vị |
| 3 | Tạo Cloze cards cho các phrase đó |
| 4 | Với từ vựng mới trong phrase, tạo thêm Vocabulary card nếu cần |
| 5 | Review hàng ngày trên Anki |

---

## ⚡ Bắt đầu nhanh

Khi bạn sẵn sàng tạo thẻ, chỉ cần:
1. Cho tôi **danh sách từ vựng** hoặc **đoạn hội thoại** bạn muốn học
2. Tôi sẽ tạo thẻ theo đúng template ở trên
3. Tự động thêm vào Anki qua `anki-agent`

> [!NOTE]
> Tài liệu này được lưu tại `artifacts/english-anki-deck-design.md` trong workspace dự án.
