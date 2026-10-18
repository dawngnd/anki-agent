# Example: Vocabulary from Topic (with Research + Review)

User nói: "Tạo cho tôi 5 từ vựng chủ đề du lịch"

## Step 1: Analyze → Card Type = Vocabulary (auto-detected)

## Step 2: Skip (card type is clear)

## Step 3: Research

Agent searches the web for each word:
- `"itinerary" definition pronunciation IPA cambridge dictionary`
- `"layover" definition pronunciation IPA`
- ...etc

## Step 4: Present Research for User Review

Agent trình bày kết quả cho user:

---

## 📝 Kết quả nghiên cứu — Từ vựng [Travel]

| # | Từ | Loại từ | Phát âm | Nghĩa | Ví dụ | Level |
|---|-----|---------|---------|-------|-------|-------|
| 1 | **itinerary** | noun | /aɪˈtɪn.ər.ər.i/ | lịch trình chuyến đi | _We planned a detailed **itinerary** for our trip._ | B2 |
| 2 | **layover** | noun | /ˈleɪ.oʊ.vɚ/ | thời gian chờ nối chuyến | _We have a 4-hour **layover** in Singapore._ | B1 |
| 3 | **check in** | phrasal verb | /tʃek ɪn/ | làm thủ tục (khách sạn/sân bay) | _You can **check in** online 24 hours before._ | A2 |
| 4 | **off the beaten track** | idiom | /ɒf ðə ˈbiː.tən træk/ | nơi ít người biết đến | _We love places **off the beaten track**._ | B2 |
| 5 | **accommodation** | noun | /əˌkɒm.əˈdeɪ.ʃən/ | chỗ ở, nơi lưu trú | _The package includes flights and **accommodation**._ | B1 |

### Chi tiết bổ sung:

**1. itinerary**
- 🔗 Collocations: travel itinerary, detailed itinerary, planned itinerary
- ⚠️ Lưu ý: Phát âm khó — /aɪˈtɪn.ər.ər.i/, nhiều người Việt đọc sai thành "ai-ti-nê-ra-ri"
- 🔄 Synonyms: schedule, travel plan, route

**2. layover**
- 🔗 Collocations: long layover, overnight layover, have a layover
- ⚠️ Lưu ý: "layover" (Mỹ) = "stopover" (Anh). "Transit" cũng dùng được nhưng ít phổ biến
- 🔄 Synonyms: stopover, transit, connection

**3. check in**
- 🔗 Collocations: check in online, check-in counter, early check-in
- ⚠️ Lưu ý: "check in" (verb) vs "check-in" (noun/adj). "Check in" ở khách sạn ≠ "check in" trên mạng xã hội
- 🔄 Antonym: check out

**4. off the beaten track**
- 🔗 Collocations: well off the beaten track, slightly off the beaten track
- ⚠️ Lưu ý: Mang nghĩa tích cực — nơi đẹp nhưng ít khách du lịch. Không phải "bị lạc"
- 🔄 Synonyms: off the beaten path (Mỹ), remote, secluded

**5. accommodation**
- 🔗 Collocations: find accommodation, budget accommodation, luxury accommodation
- ⚠️ Lưu ý: Thường dùng số ít (uncountable) ở British English. "Accommodations" (số nhiều) phổ biến ở American English
- 🔄 Synonyms: lodging, housing, place to stay

---
> Bạn muốn chỉnh sửa gì không? Có thể:
> - ❌ Bỏ từ nào không muốn học
> - ✏️ Sửa nghĩa / ví dụ
> - ➕ Thêm từ mới
> - ✅ OK — Tạo thẻ Anki

---

## Step 5: User Feedback

User: "✅ OK, tạo đi"

## Step 6: Deck Selection

```bash
anki-agent deck list
```

User chọn `English::Vocabulary` (hoặc agent tạo mới nếu chưa có).

## Step 7: Generate & Insert Cards

Agent dùng ĐÚNG nội dung đã review để tạo JSON:

```json
[
  {
    "deck": "English::Vocabulary",
    "model": "Basic",
    "fields": {
      "Front": "<p style='font-size:1.5em'><strong>itinerary</strong></p><p><em>noun</em></p>",
      "Back": "<p><strong>Phát âm:</strong> /aɪˈtɪn.ər.ər.i/</p><p><strong>Nghĩa:</strong> lịch trình, kế hoạch chuyến đi</p><hr><p><strong>Ví dụ:</strong></p><p><em>We planned a detailed <u>itinerary</u> for our two-week trip to Japan.</em></p><p>Chúng tôi đã lên lịch trình chi tiết cho chuyến đi hai tuần đến Nhật Bản.</p><hr><p><strong>Collocations:</strong> travel itinerary, detailed itinerary</p>"
    },
    "tags": ["type::vocab", "topic::travel", "level::B2", "ai-generated"]
  },
  {
    "deck": "English::Vocabulary",
    "model": "Basic",
    "fields": {
      "Front": "<p style='font-size:1.5em'><strong>layover</strong></p><p><em>noun</em></p>",
      "Back": "<p><strong>Phát âm:</strong> /ˈleɪ.oʊ.vɚ/</p><p><strong>Nghĩa:</strong> thời gian chờ nối chuyến (tại sân bay)</p><hr><p><strong>Ví dụ:</strong></p><p><em>We have a 4-hour <u>layover</u> in Singapore before our connecting flight.</em></p><p>Chúng tôi có 4 giờ chờ nối chuyến ở Singapore trước chuyến bay tiếp theo.</p><hr><p><strong>Collocations:</strong> long layover, overnight layover</p>"
    },
    "tags": ["type::vocab", "topic::travel", "level::B1", "ai-generated"]
  }
]
```

_(JSON đầy đủ cho tất cả 5 từ)_

```bash
cat <<'EOF' | anki-agent note add-many --file -
[...JSON above...]
EOF
```

## Step 8: Verify & Report

```bash
anki-agent note find --query "tag:ai-generated tag:topic::travel added:1" --details
anki-agent sync
```

> ✅ Đã tạo **5 thẻ từ vựng** chủ đề du lịch trong deck `English::Vocabulary`
> Các từ: itinerary, layover, check in, off the beaten track, accommodation
