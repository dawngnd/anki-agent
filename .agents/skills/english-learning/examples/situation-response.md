# Example: Situation Response Cards

User nói: "Tạo thẻ phản xạ tình huống cho các tình huống ở nhà hàng"

## Step 1: Analyze → Card Type = Situation Response (auto-detected)

## Step 2: Deck Selection

User chọn `English::Phrases`

## Step 3: Generate Cards

```json
[
  {
    "deck": "English::Phrases",
    "model": "Basic",
    "fields": {
      "Front": "<p><strong>🎭 Situation:</strong></p><p>Bạn đến nhà hàng và muốn <strong>xin bàn cho 2 người</strong>.</p><p><em>Nói bằng tiếng Anh?</em></p>",
      "Back": "<p><strong>Cách nói tự nhiên:</strong></p><p style='font-size:1.2em'><em>\"Hi, table for two, please.\"</em></p><hr><p><strong>Các cách khác:</strong></p><ul><li>\"Could we get a table for two?\"</li><li>\"We have a reservation under [name] for two.\" (nếu đã đặt trước)</li></ul><p><strong>Lưu ý:</strong> Đơn giản nhất là 'Table for two, please.' — không cần câu dài.</p>"
    },
    "tags": ["type::situation", "situation::ordering", "level::A2", "ai-generated"]
  },
  {
    "deck": "English::Phrases",
    "model": "Basic",
    "fields": {
      "Front": "<p><strong>🎭 Situation:</strong></p><p>Bạn muốn <strong>gọi món</strong> nhưng chưa quyết định được.</p><p><em>Nói bằng tiếng Anh?</em></p>",
      "Back": "<p><strong>Cách nói tự nhiên:</strong></p><p style='font-size:1.2em'><em>\"Could you give us a few more minutes, please? We haven't decided yet.\"</em></p><hr><p><strong>Các cách khác:</strong></p><ul><li>\"We need a bit more time, please.\"</li><li>\"Sorry, we're still looking at the menu.\"</li></ul><p><strong>Lưu ý:</strong> Tránh nói 'Wait!' — thiếu lịch sự. Luôn thêm 'please'.</p>"
    },
    "tags": ["type::situation", "situation::ordering", "level::A2", "ai-generated"]
  },
  {
    "deck": "English::Phrases",
    "model": "Basic",
    "fields": {
      "Front": "<p><strong>🎭 Situation:</strong></p><p>Bạn muốn <strong>hỏi nhân viên giới thiệu món</strong> ngon.</p><p><em>Nói bằng tiếng Anh?</em></p>",
      "Back": "<p><strong>Cách nói tự nhiên:</strong></p><p style='font-size:1.2em'><em>\"What do you recommend?\"</em></p><hr><p><strong>Các cách khác:</strong></p><ul><li>\"What's your most popular dish?\"</li><li>\"What would you suggest for someone who likes seafood?\"</li><li>\"Is there anything you'd particularly recommend?\"</li></ul><p><strong>Lưu ý:</strong> 'What do you recommend?' là cách nói ngắn gọn và tự nhiên nhất.</p>"
    },
    "tags": ["type::situation", "situation::ordering", "level::A2", "ai-generated"]
  },
  {
    "deck": "English::Phrases",
    "model": "Basic",
    "fields": {
      "Front": "<p><strong>🎭 Situation:</strong></p><p>Bạn bị <strong>dị ứng thực phẩm</strong> và muốn hỏi về thành phần món ăn.</p><p><em>Nói bằng tiếng Anh?</em></p>",
      "Back": "<p><strong>Cách nói tự nhiên:</strong></p><p style='font-size:1.2em'><em>\"I have a nut allergy. Does this dish contain any nuts?\"</em></p><hr><p><strong>Các cách khác:</strong></p><ul><li>\"Could you check if this is gluten-free?\"</li><li>\"I'm allergic to shellfish. Is there any in this dish?\"</li><li>\"Are there any allergens I should know about?\"</li></ul><p><strong>Lưu ý:</strong> Nói rõ loại dị ứng trước, rồi hỏi về món ăn. Đây là vấn đề sức khỏe — đừng ngại hỏi kỹ.</p>"
    },
    "tags": ["type::situation", "situation::ordering", "situation::health", "level::B1", "ai-generated"]
  },
  {
    "deck": "English::Phrases",
    "model": "Basic",
    "fields": {
      "Front": "<p><strong>🎭 Situation:</strong></p><p>Bạn muốn <strong>xin hóa đơn / thanh toán</strong>.</p><p><em>Nói bằng tiếng Anh?</em></p>",
      "Back": "<p><strong>Cách nói tự nhiên:</strong></p><p style='font-size:1.2em'><em>\"Could we get the check, please?\"</em></p><hr><p><strong>Các cách khác:</strong></p><ul><li>\"Could I have the bill, please?\" (British English)</li><li>\"We're ready to pay.\"</li><li>\"Can we settle up?\" (informal)</li></ul><p><strong>Lưu ý:</strong> 'check' (Mỹ) vs 'bill' (Anh) — cả hai đều đúng. Khi muốn trả riêng: 'Could we split the bill?'</p>"
    },
    "tags": ["type::situation", "situation::ordering", "level::A2", "ai-generated"]
  }
]
```

## Step 4: Execute

```bash
cat <<'EOF' | anki-agent note add-many --file -
[...JSON above...]
EOF
```

## Step 5: Verify & Report

```bash
anki-agent note find --query "tag:ai-generated tag:type::situation added:1" --details
anki-agent sync
```

> ✅ Đã tạo **5 thẻ phản xạ tình huống** nhà hàng trong deck `English::Phrases`
> Bao gồm: xin bàn, gọi món, hỏi gợi ý, dị ứng thực phẩm, thanh toán
