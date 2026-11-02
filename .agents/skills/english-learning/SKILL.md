---
name: english-learning
description: >-
  Creates English learning Anki flashcards from user-provided vocabulary,
  phrases, grammar rules, conversation scripts, or tips. Supports 4 dedicated
  models: English_Grammar, English_Vocab, English_Phrase_Reflex, and English_Tip.
  Handles deck selection (defaulting to English_v0.0.1 subdecks), research,
  audio integration, and bulk insertion via anki-agent CLI. Use when the user
  wants to learn English grammar, vocabulary, phrases, or test-taking tips.
---

# English Learning Flashcard Skill (v0.0.1 Architecture)

## Overview

This skill creates high-quality English learning flashcards for Vietnamese learners. It operates on a **4-pillar architecture** utilizing dedicated custom Anki models (clean data fields, responsive Modern UI, Dark/Light mode support):

| Category | Model Name | Goal & Learning Interaction | Target Deck |
|---|---|---|---|
| **1. Ngữ pháp (Grammar)** | `English_Grammar` | Nhìn tên chủ điểm/định nghĩa, người học phải tự trình bày bản chất quy tắc, công thức và ví dụ. | `English_v0.0.1::Grammar` |
| **2. Từ vựng (Vocabulary)** | `English_Vocab` | Nhìn mặt từ tiếng Anh, phản xạ 3 bước: đọc to phát âm, nói ý nghĩa, tự đặt 1 câu ví dụ trước khi lật mặt sau. | `English_v0.0.1::Vocabulary` |
| **3. Cụm từ & Phản xạ (Phrase Reflex)** | `English_Phrase_Reflex` | Đọc bối cảnh giao tiếp + lời đối phương (Speaker A) + gợi ý ý định, phản xạ đáp lại bằng Cụm từ mục tiêu. | `English_v0.0.1::Phrases` |
| **4. Ghi chú & Mẹo (Notes / Tips)** | `English_Tip` | Nhìn tên mẹo/bẫy đề thi, lập tức tái hiện câu thần chú (mnemonic), các lỗi bẫy cần tránh (Wrong vs Right). | `English_v0.0.1::Notes` |

> [!TIP]
> **Cấu hình Deck Gốc (`DECK_ROOT`)**: Mặc định hiện tại là `English_v0.0.1`. Khi người dùng xác nhận đã kiểm chứng xong và muốn đưa về chính thức, chỉ cần đổi `DECK_ROOT = "English"`.

---

## Workflow (Quy Trình 8 Bước Chuẩn)

> [!IMPORTANT]
> **Nguyên tắc bất di bất dịch**: KHÔNG BAO GIỜ tự động tạo thẻ vào Anki khi người dùng chưa xem và xác nhận kết quả nghiên cứu.
> Quy trình luôn là: **Analyze → Research → Present Review → User Feedback → Insert Cards → Verify**.

### Bước 1: Phân Loại Đầu Vào (Analyze User Input)

Khi người dùng cung cấp tài liệu hoặc yêu cầu học, phân loại vào 1 trong 4 nhóm:

| Đầu vào | Ví dụ | → Model & Deck |
|---|---|---|
| Quy tắc ngữ pháp, cấu trúc câu, thì, mệnh đề | "học về câu điều kiện loại 3", "quy tắc hòa hợp S-V" | `English_Grammar` → `...::Grammar` |
| Danh sách từ vựng đơn lẻ, từ theo chủ đề | "từ vựng về hợp đồng", "learn: resilient, ambiguous" | `English_Vocab` → `...::Vocabulary` |
| Cụm từ, thành ngữ, đoạn hội thoại, tình huống | "cách xin thêm thời gian suy nghĩ", "take a moment to" | `English_Phrase_Reflex` → `...::Phrases` |
| Mẹo làm bài thi (TOEIC, IELTS), bẫy đề thi, mẹo nhớ | "bẫy danh từ không đếm được", "phân biệt while vs when" | `English_Tip` → `...::Notes` |
| Hỗn hợp | Bài đọc có từ mới, ngữ pháp và cụm từ hay | Phân tách và tạo đúng loại tương ứng |

---

### Bước 2: Xác Nhận Thể Loại (Nếu Chưa Rõ Ràng)

Nếu đầu vào chưa rõ loại thẻ muốn tạo, hỏi người dùng:

> Bạn muốn tạo thẻ học theo dạng nào sau đây?
>
> 1. 📘 **Ngữ pháp (Grammar)** — Định nghĩa, công thức cấu trúc, bẫy và ví dụ câu
> 2. 📗 **Từ vựng (Vocabulary)** — Thẻ từ vựng có checklist phản xạ 3 bước, audio và collocations
> 3. 📙 **Cụm từ / Phản xạ hội thoại (Phrase Reflex)** — Đoạn đối đáp 2 người (Speaker A & You) có ngữ cảnh
> 4. 📒 **Ghi chú & Mẹo (Tip & Trick)** — Tên mẹo thi, câu thần chú ghi nhớ và bẫy sai thường gặp
> 5. 🔄 **Kết hợp** — Tự động phân loại phù hợp cho từng mục

---

### Bước 3: Nghiên Cứu Chi Tiết (Research Protocol)

Agent bắt buộc phải tra cứu chính xác từ các nguồn uy tín trước khi soạn thảo thẻ:

1. **Từ vựng (Vocab)**:
   - Tra cứu phiên âm IPA và audio phát âm giọng Mỹ/Anh từ **Oxford Learner's Dictionaries** (`oxfordlearnersdictionaries.com`).
   - Tra cứu Collocations tự nhiên qua từ điển Oxford Collocations Dictionary hoặc OZDIC.
   - Xác định cấp độ CEFR (`level::B1`, `level::B2`, etc.).

2. **Cụm từ / Mẫu câu (Phrase Reflex)**:
   - **Quy tắc Bộ 3 Ngữ Cảnh Bắt Buộc (3-Pillar Context Rule)**:
     - `Context`: Bối cảnh chi tiết 1-2 câu (Địa điểm/không gian + Ai nói với ai + Tình huống phát sinh). Tuyệt đối không chỉ để mỗi nhãn danh mục ngắn ngủi. (VD: `🏢 Văn phòng: Bạn đang ngồi làm việc thì đồng nghiệp ghé bàn muốn trao đổi gấp tài liệu, đúng lúc bạn có điện thoại khẩn.`).
     - `Speaker_A`: Lời thoại mào đầu / kích hoạt tự nhiên từ đối phương (Colleague, Manager, Waiter, Examiner, Friend). Phải là câu nói/câu hỏi đời thực, gắn chặt với hoàn cảnh.
     - `Learner_Intention`: Ý định phản hồi của người học bằng tiếng Việt rõ ràng, biểu cảm.
   - **CẤM Tuyệt Đối Canned Questions**: Tuyệt đối KHÔNG dùng các câu hỏi rập khuôn, chung chung như: *"Could you tell me more about how you handle this situation?"*, *"Can you elaborate on that?"*, *"Can you handle this in English?"*. Lời thoại Speaker A phải là chất xúc tác trực tiếp để người học bật ra câu trả lời chứa Target Phrase.
   - Cung cấp gợi ý từ đầu (`Hint`), câu phản xạ trọn vẹn (`Full_Response`) và 2-3 cách diễn đạt thay thế (`Alternative_Responses`).

3. **Ngữ pháp (Grammar)**:
   - Tóm lược bản chất quy tắc ngắn gọn, dễ hiểu.
   - Sơ đồ hóa công thức rõ ràng.
   - Đưa ra bẫy thi thường gặp hoặc ngoại lệ hay gây nhầm lẫn.

4. **Mẹo & Bẫy (Tip)**:
   - Tạo tên mẹo ngắn gọn, ấn tượng.
   - Đúc kết thành câu thần chú / quy tắc nhớ nhanh (Mnemonic).
   - Minh họa bảng đối chiếu ❌ Câu sai (Wrong) vs ✅ Câu đúng (Right).

---

### Bước 4: Trình Bày Cho Người Dùng Review (Review Presentation)

Trình bày bảng tóm tắt và chi tiết các thẻ dự kiến tạo theo mẫu sau:

```markdown
## 📝 Kết Quả Nghiên Cứu Flashcards (Deck: English_v0.0.1)

| # | Loại thẻ | Mục tiêu học / Từ vựng | Ý nghĩa / Quy tắc cốt lõi | Level |
|---|---|---|---|---|
| 1 | 📗 Vocab | **contract** (n) | Hợp đồng, giao kèo pháp lý | B1 |
| 2 | 📙 Phrase | **take a moment to** | Dành một chút thời gian để làm gì | B1 |
| 3 | 📘 Grammar | **Hòa hợp S - V với "N1 + of + N2"** | Động từ luôn chia theo N1 (Chủ ngữ thật) | B1 |
| 4 | 📒 Tip | **Bẫy danh từ không đếm được** | Không có -s/-es, luôn chia động từ số ít | B1 |

---
> Bạn có muốn điều chỉnh gì không?
> - ✏️ Chỉnh sửa nghĩa / ví dụ
> - ❌ Bỏ bớt thẻ không cần thiết
> - ➕ Thêm thẻ mới
> - ✅ OK — Bắt đầu nạp thẻ vào Anki
```

---

### Bước 5: Tiếp Nhận Phản Hồi & Hoàn Thiện

Chỉ khi người dùng xác nhận **"OK"** hoặc **"Tạo thẻ đi"**, agent mới tiến hành chèn thẻ vào Anki. Nếu có chỉnh sửa, cập nhật lại và hiển thị danh sách cuối cùng.

---

### Bước 6: Chèn Thẻ Vào Anki Bằng CLI (Bulk Insert)

Sử dụng `anki-agent note add-many --file -` với cấu trúc JSON chuẩn cho từng model:

```bash
cat <<'EOF' | uv run anki-agent note add-many --file -
[
  {
    "deck": "English_v0.0.1::Vocabulary",
    "model": "English_Vocab",
    "fields": {
      "Word": "contract",
      "PartOfSpeech": "noun",
      "Phonetic_IPA": "ˈkɑːn.trækt",
      "Audio": "[sound:contract_us.mp3]",
      "Vietnamese_Meaning": "Hợp đồng, giao kèo pháp lý",
      "Collocations": "sign a contract, breach a contract, negotiate a contract",
      "Example_Sentence": "Both companies signed a two-year <u>contract</u> yesterday.",
      "Example_Translation": "Cả hai công ty đã ký một hợp đồng có thời hạn hai năm vào ngày hôm qua.",
      "Image": ""
    },
    "tags": ["type::vocab", "topic::business", "level::B1", "ai-generated"]
  }
]
EOF
```

---

### Bước 7: Kiểm Tra & Đồng Bộ (Verify & Sync)

```bash
uv run anki-agent note find --query "deck:English_v0.0.1 tag:ai-generated added:1" --details
uv run anki-agent sync
```

---

## Chi Tiết Các Model & Trường Dữ Liệu (Field Specs)

### 1. Model: `English_Grammar`
- **Deck**: `English_v0.0.1::Grammar`
- **Fields**:
  - `Title`: Tên chủ điểm / Quy tắc ngữ pháp (VD: `[Quy tắc] Hòa hợp S - V với cụm "N1 + of + N2"`)
  - `Prompt`: Câu hỏi phản xạ ở mặt trước (VD: `Trong cấu trúc N1 + of + N2 + V, động từ chia theo N1 hay N2? Cho ví dụ?`)
  - `Core_Rule`: Quy tắc cốt lõi ngắn gọn
  - `Formula_Structure`: Công thức / sơ đồ cấu trúc
  - `Explanation`: Giải thích chi tiết và phân tích
  - `Examples`: Câu ví dụ thực tế minh họa
  - `Common_Pitfalls`: Bẫy đề thi hoặc các trường hợp ngoại lệ

### 2. Model: `English_Vocab`
- **Deck**: `English_v0.0.1::Vocabulary`
- **Fields**:
  - `Word`: Từ tiếng Anh
  - `PartOfSpeech`: Từ loại (noun, verb, adjective, adverb...)
  - `Phonetic_IPA`: Phiên âm quốc tế (không cần dấu gạch chéo `/ /`)
  - `Audio`: Cú pháp file âm thanh `[sound:{word}_us.mp3]`
  - `Vietnamese_Meaning`: Nghĩa tiếng Việt
  - `Collocations`: Cụm từ hay đi kèm
  - `Example_Sentence`: Câu ví dụ chứa từ (gạch chân từ bằng thẻ `<u>`)
  - `Example_Translation`: Dịch câu ví dụ sang tiếng Việt
  - `Image`: Thẻ ảnh `<img src="...">` (nếu có)

### 3. Model: `English_Phrase_Reflex`
- **Deck**: `English_v0.0.1::Phrases`
- **Fields**:
  - `Context`: Bối cảnh / Tình huống giao tiếp chi tiết 1-2 câu (VD: `🏢 Văn phòng: Bạn đang ngồi làm việc thì đồng nghiệp ghé bàn muốn trao đổi gấp tài liệu, đúng lúc bạn có điện thoại khẩn.`)
  - `Speaker_A`: Lời thoại mào đầu / câu hỏi trực tiếp của đối phương (VD: `Colleague: "Hey, do you have a quick minute to look over this report with me?"`)
  - `Learner_Intention`: Ý định phản hồi của người học bằng tiếng Việt (VD: `Bạn muốn nói: Tôi cần tạm rời bàn làm việc mấy phút để nghe một cuộc điện thoại khẩn cấp.`)
  - `Hint`: Gợi ý từ đầu (VD: `step away fr...`)
  - `Target_Phrase`: Cụm từ mục tiêu cần học (VD: `step away from`)
  - `Audio`: File âm thanh phát âm cụm từ / câu nếu có
  - `Full_Response`: Câu phản xạ hoàn chỉnh bằng tiếng Anh (VD: `"I need to step away from my desk for a few minutes to take an urgent phone call."`)
  - `Meaning_Usage`: Giải nghĩa cụm từ, phiên âm IPA, collocations và ngữ cảnh sử dụng
  - `Alternative_Responses`: Danh sách các biến thể tự nhiên khác (`<ul><li>...</li></ul>`)

### 4. Model: `English_Tip`
- **Deck**: `English_v0.0.1::Notes`
- **Fields**:
  - `Tip_Name`: Tên mẹo / Khái niệm bẫy
  - `Category`: Phân loại (VD: `TOEIC Part 5 / Ngữ pháp`)
  - `Prompt`: Câu hỏi gợi nhớ ở mặt trước
  - `Core_Rule`: Quy tắc vàng / Câu thần chú ghi nhớ
  - `Common_Mistakes`: Bảng bẫy thường gặp (❌ Sai vs ✅ Đúng)
  - `Example_Analysis`: Phân tích ví dụ thực tế
