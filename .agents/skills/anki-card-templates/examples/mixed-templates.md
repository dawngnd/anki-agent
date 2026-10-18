# Complete Example: Mixed Templates

Ví dụ thực tế khi user nói: "Tạo flashcard về Python async/await"

## Step 1: Agent hỏi chọn template

> Bạn muốn dùng template nào cho các thẻ flashcard?
> 1. **Basic Q&A** — Câu hỏi / trả lời đơn giản
> 2. **Vocabulary** — Từ vựng ngôn ngữ
> 3. **Cloze Deletion** — Điền vào chỗ trống
> 4. **Code** — Code snippet / lập trình
> 5. **Concept Definition** — Khái niệm / định nghĩa
> 6. **Comparison** — So sánh hai thứ
> 7. **Process / Steps** — Quy trình / các bước

User chọn: "Kết hợp Code + Concept + Cloze"

## Step 2: Agent hỏi chọn deck

```bash
anki-agent deck list
```
→ User chọn deck "Programming::Python"

## Step 3: Agent tạo cards theo template đã chọn

```json
[
  {
    "deck": "Programming::Python",
    "model": "Basic",
    "fields": {
      "Front": "<p style='font-size:1.3em'><strong>async/await</strong></p><p><em>Python Concurrency</em></p>",
      "Back": "<p><strong>Definition:</strong> Keywords for writing asynchronous code that can pause and resume execution without blocking the thread.</p><ul><li><code>async def</code> defines a coroutine function</li><li><code>await</code> pauses execution until the awaited coroutine completes</li><li>Runs on an event loop (e.g., <code>asyncio</code>)</li></ul><hr><p><strong>Example:</strong> <code>await asyncio.sleep(1)</code> pauses for 1 second without blocking other tasks.</p>"
    },
    "tags": ["python", "async", "concurrency", "concept", "ai-generated"]
  },
  {
    "deck": "Programming::Python",
    "model": "Basic",
    "fields": {
      "Front": "<p><strong>[Python]</strong></p><p>Write an async function that fetches data from a URL using aiohttp.</p>",
      "Back": "<pre><code>import aiohttp\nimport asyncio\n\nasync def fetch(url):\n    async with aiohttp.ClientSession() as session:\n        async with session.get(url) as resp:\n            return await resp.text()\n\n# Run it\nresult = asyncio.run(fetch('https://example.com'))</code></pre><p><strong>Key:</strong> <code>async with</code> ensures the session/response is properly closed.</p>"
    },
    "tags": ["python", "async", "aiohttp", "code", "ai-generated"]
  },
  {
    "deck": "Programming::Python",
    "model": "Cloze",
    "fields": {
      "Text": "<p>In Python, <code>{{c1::async def}}</code> defines a coroutine, and <code>{{c2::await}}</code> is used to pause execution until the coroutine completes. Coroutines run on an {{c3::event loop}}.</p>",
      "Extra": "<p>Use <code>asyncio.run()</code> to start the event loop from synchronous code.</p>"
    },
    "tags": ["python", "async", "cloze", "ai-generated"]
  },
  {
    "deck": "Programming::Python",
    "model": "Basic",
    "fields": {
      "Front": "<p><strong>Threading</strong> vs <strong>asyncio</strong></p><p><em>Python concurrency models</em></p>",
      "Back": "<table border='1' cellpadding='6' cellspacing='0' style='border-collapse:collapse;width:100%'><tr style='background:#f0f0f0'><th></th><th>Threading</th><th>asyncio</th></tr><tr><td><strong>Model</strong></td><td>Preemptive multitasking</td><td>Cooperative multitasking</td></tr><tr><td><strong>GIL impact</strong></td><td>Limited by GIL for CPU</td><td>Single thread, no GIL issue</td></tr><tr><td><strong>Best for</strong></td><td>I/O-bound with blocking libs</td><td>I/O-bound with async libs</td></tr><tr><td><strong>Overhead</strong></td><td>Higher (thread switching)</td><td>Lower (coroutine switching)</td></tr></table><p><strong>Use threading</strong> with legacy blocking I/O. <strong>Use asyncio</strong> for new I/O-heavy apps.</p>"
    },
    "tags": ["python", "async", "threading", "comparison", "ai-generated"]
  }
]
```

## Step 4: Execute

```bash
cat <<'EOF' | anki-agent note add-many --file -
[... JSON trên ...]
EOF
```

## Step 5: Verify & Report

```bash
anki-agent note find --query "tag:ai-generated tag:python tag:async" --details
anki-agent sync
```
