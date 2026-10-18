---
name: anki-card-templates
description: >-
  Designs and formats Anki flashcard content using proven templates.
  Use when generating flashcards to ensure consistent, high-quality card
  design. Use before calling anki-agent note add or add-many to structure
  the card content properly. Covers vocabulary, cloze, code, concept,
  comparison, and process card types.
---

# Anki Card Templates

## Overview

This skill defines **card templates** that the agent MUST follow when creating
Anki flashcards. Templates ensure cards follow spaced-repetition best practices:
atomic, clear, and optimally formatted for learning.

## Template Selection Procedure

> [!IMPORTANT]
> **Before generating any cards**, follow this procedure:
>
> 1. **Analyze the content** the user wants to learn
> 2. **Present available templates** to the user and ask which to use
> 3. **Wait for user selection** — never auto-pick a template
> 4. **Generate cards** following the selected template exactly

### Presenting Templates to User

When the user asks to create flashcards, present this selection:

> Bạn muốn dùng template nào cho các thẻ flashcard?
>
> 1. **Basic Q&A** — Câu hỏi / trả lời đơn giản
> 2. **Vocabulary** — Từ vựng ngôn ngữ (từ, phiên âm, nghĩa, ví dụ)
> 3. **Cloze Deletion** — Điền vào chỗ trống
> 4. **Code** — Code snippet / lập trình
> 5. **Concept Definition** — Khái niệm / định nghĩa
> 6. **Comparison** — So sánh hai thứ
> 7. **Process / Steps** — Quy trình / các bước

---

## Templates

### 1. Basic Q&A

**Model**: `Basic`
**Use for**: Factual knowledge, simple recall

**Rules**:
- Front: ONE specific question — never vague or too broad
- Back: Concise answer — maximum 2-3 sentences
- Add context only if absolutely necessary

**Format**:
```json
{
  "model": "Basic",
  "fields": {
    "Front": "<p><strong>Question here?</strong></p>",
    "Back": "<p>Answer here.</p>"
  }
}
```

**Good example**:
```json
{
  "fields": {
    "Front": "<p>What is the time complexity of binary search?</p>",
    "Back": "<p><strong>O(log n)</strong></p><p>The search space is halved with each step.</p>"
  }
}
```

**Bad example** (too vague):
```json
{
  "fields": {
    "Front": "Tell me about binary search",
    "Back": "Binary search is an algorithm that..."
  }
}
```

---

### 2. Vocabulary

**Model**: `Basic`
**Use for**: Language learning (any language pair)

**Rules**:
- Front: The word/phrase in the target language
- Back: Structured with pronunciation, meaning, example sentence
- Use HTML formatting for visual hierarchy
- Always include an example sentence with the word in context

**Format**:
```json
{
  "model": "Basic",
  "fields": {
    "Front": "<p style='font-size:1.5em'><strong>word</strong></p><p><em>part of speech</em></p>",
    "Back": "<p><strong>Pronunciation:</strong> /phonetic/</p><p><strong>Meaning:</strong> definition</p><hr><p><strong>Example:</strong></p><p><em>Example sentence with <u>word</u> underlined.</em></p><p>Translation of example.</p>"
  }
}
```

**Example — Japanese**:
```json
{
  "fields": {
    "Front": "<p style='font-size:1.5em'><strong>食べる</strong></p><p><em>動詞 (verb)</em></p>",
    "Back": "<p><strong>Reading:</strong> たべる (taberu)</p><p><strong>Meaning:</strong> to eat</p><hr><p><strong>Example:</strong></p><p><em>毎朝パンを<u>食べる</u>。</em></p><p>I eat bread every morning.</p>"
  }
}
```

**Example — English for Vietnamese speakers**:
```json
{
  "fields": {
    "Front": "<p style='font-size:1.5em'><strong>resilient</strong></p><p><em>adjective</em></p>",
    "Back": "<p><strong>Phát âm:</strong> /rɪˈzɪl.i.ənt/</p><p><strong>Nghĩa:</strong> kiên cường, có khả năng phục hồi nhanh</p><hr><p><strong>Ví dụ:</strong></p><p><em>Children are remarkably <u>resilient</u> — they bounce back quickly from setbacks.</em></p><p>Trẻ em rất kiên cường — chúng phục hồi nhanh chóng sau những thất bại.</p>"
  }
}
```

---

### 3. Cloze Deletion

**Model**: `Cloze`
**Use for**: Key terms within context, formulas, fill-in-the-blank

**Rules**:
- Each `{{c1::...}}` creates one card — use separate cloze numbers for separate facts
- Keep surrounding context meaningful — don't cloze random words
- Add hint after `::` if the cloze is ambiguous: `{{c1::answer::hint}}`
- Use the `Extra` field for additional explanation

**Format**:
```json
{
  "model": "Cloze",
  "fields": {
    "Text": "<p>Sentence with {{c1::cloze deletion}} in context.</p>",
    "Extra": "<p>Additional explanation or source.</p>"
  }
}
```

**Example — Science**:
```json
{
  "fields": {
    "Text": "<p>The {{c1::mitochondria}} is the {{c2::powerhouse}} of the cell, responsible for producing {{c3::ATP}}.</p>",
    "Extra": "<p>ATP = Adenosine Triphosphate. Mitochondria convert nutrients into energy through cellular respiration.</p>"
  }
}
```

**Example — Programming**:
```json
{
  "fields": {
    "Text": "<p>In Python, {{c1::list comprehension}} syntax is: <code>[{{c2::expression}} for {{c3::item}} in {{c4::iterable}}]</code></p>",
    "Extra": "<p>Example: <code>[x**2 for x in range(10)]</code></p>"
  }
}
```

---

### 4. Code

**Model**: `Basic`
**Use for**: Programming concepts, syntax, algorithms

**Rules**:
- Front: Describe what the code should do (in natural language)
- Back: Show the code with syntax highlighting via `<pre><code>`
- Always specify the language
- Keep code snippets SHORT — max 5-10 lines per card
- One concept per card — never combine multiple techniques

**Format**:
```json
{
  "model": "Basic",
  "fields": {
    "Front": "<p><strong>[Language]</strong></p><p>Description of what to write/do.</p>",
    "Back": "<pre><code>code here</code></pre><p><strong>Explanation:</strong> Brief note.</p>"
  }
}
```

**Example**:
```json
{
  "fields": {
    "Front": "<p><strong>[Python]</strong></p><p>How do you define a decorator that logs function calls?</p>",
    "Back": "<pre><code>def log_calls(func):\n    def wrapper(*args, **kwargs):\n        print(f'Calling {func.__name__}')\n        return func(*args, **kwargs)\n    return wrapper\n\n@log_calls\ndef greet(name):\n    return f'Hello, {name}'</code></pre><p><strong>Key:</strong> A decorator is a function that takes a function and returns a modified function.</p>"
  }
}
```

---

### 5. Concept Definition

**Model**: `Basic`
**Use for**: Academic terms, technical concepts, definitions

**Rules**:
- Front: The term/concept name only
- Back: Structured with definition, key characteristics, and a concrete example
- Use bullet points for characteristics
- Always end with a concrete, memorable example

**Format**:
```json
{
  "model": "Basic",
  "fields": {
    "Front": "<p style='font-size:1.3em'><strong>Term / Concept</strong></p><p><em>Category or field</em></p>",
    "Back": "<p><strong>Definition:</strong> Clear, concise definition.</p><ul><li>Key characteristic 1</li><li>Key characteristic 2</li><li>Key characteristic 3</li></ul><hr><p><strong>Example:</strong> Concrete, memorable example.</p>"
  }
}
```

**Example**:
```json
{
  "fields": {
    "Front": "<p style='font-size:1.3em'><strong>Dependency Injection</strong></p><p><em>Software Design Pattern</em></p>",
    "Back": "<p><strong>Definition:</strong> A technique where an object receives its dependencies from external sources rather than creating them internally.</p><ul><li>Decouples components — easier to test and maintain</li><li>Dependencies are \"injected\" via constructor, setter, or interface</li><li>Enables swapping implementations without changing the class</li></ul><hr><p><strong>Example:</strong> Instead of <code>self.db = Database()</code>, pass it in: <code>def __init__(self, db): self.db = db</code></p>"
  }
}
```

---

### 6. Comparison

**Model**: `Basic`
**Use for**: Comparing two or more concepts, tools, approaches

**Rules**:
- Front: "What is the difference between X and Y?" or "X vs Y"
- Back: Use an HTML table for clear side-by-side comparison
- Include a summary row or sentence at the bottom
- Maximum 4-5 comparison dimensions

**Format**:
```json
{
  "model": "Basic",
  "fields": {
    "Front": "<p><strong>X</strong> vs <strong>Y</strong></p><p><em>What's the difference?</em></p>",
    "Back": "<table border='1' cellpadding='6' cellspacing='0' style='border-collapse:collapse;width:100%'><tr style='background:#f0f0f0'><th></th><th>X</th><th>Y</th></tr><tr><td><strong>Aspect 1</strong></td><td>...</td><td>...</td></tr><tr><td><strong>Aspect 2</strong></td><td>...</td><td>...</td></tr><tr><td><strong>Aspect 3</strong></td><td>...</td><td>...</td></tr></table><p><strong>Summary:</strong> When to use each.</p>"
  }
}
```

**Example**:
```json
{
  "fields": {
    "Front": "<p><strong>REST</strong> vs <strong>GraphQL</strong></p><p><em>API design approaches</em></p>",
    "Back": "<table border='1' cellpadding='6' cellspacing='0' style='border-collapse:collapse;width:100%'><tr style='background:#f0f0f0'><th></th><th>REST</th><th>GraphQL</th></tr><tr><td><strong>Data fetching</strong></td><td>Multiple endpoints</td><td>Single endpoint, query-based</td></tr><tr><td><strong>Over-fetching</strong></td><td>Common issue</td><td>Client requests exact fields</td></tr><tr><td><strong>Caching</strong></td><td>HTTP caching built-in</td><td>More complex, needs custom</td></tr><tr><td><strong>Learning curve</strong></td><td>Simple, well-known</td><td>Steeper, schema-first</td></tr></table><p><strong>Use REST</strong> for simple CRUD APIs. <strong>Use GraphQL</strong> when clients need flexible queries.</p>"
  }
}
```

---

### 7. Process / Steps

**Model**: `Basic`
**Use for**: Procedures, algorithms, step-by-step instructions

**Rules**:
- Front: "How do you [process]?" or "What are the steps to [goal]?"
- Back: Numbered steps with brief explanation for each
- Maximum 5-7 steps per card — split longer processes into multiple cards
- Add a mnemonic or summary if possible

**Format**:
```json
{
  "model": "Basic",
  "fields": {
    "Front": "<p>What are the steps to <strong>[process]</strong>?</p>",
    "Back": "<ol><li><strong>Step 1:</strong> Description</li><li><strong>Step 2:</strong> Description</li><li><strong>Step 3:</strong> Description</li></ol><hr><p><strong>Remember:</strong> Mnemonic or key takeaway.</p>"
  }
}
```

**Example**:
```json
{
  "fields": {
    "Front": "<p>What are the steps of the <strong>TDD (Test-Driven Development)</strong> cycle?</p>",
    "Back": "<ol><li><strong style='color:red'>RED:</strong> Write a failing test that defines the desired behavior</li><li><strong style='color:green'>GREEN:</strong> Write the minimum code to make the test pass</li><li><strong style='color:blue'>REFACTOR:</strong> Improve the code while keeping tests green</li></ol><hr><p><strong>Remember:</strong> 🔴 Red → 🟢 Green → 🔵 Refactor → Repeat</p>"
  }
}
```

---

## Card Design Best Practices

> [!TIP]
> Follow these rules for ALL templates:

1. **Atomic cards** — One fact per card. If a card has "and" in the answer, split it.
2. **No orphan cards** — Every card should connect to a broader topic via tags.
3. **Use HTML** — Anki renders HTML. Use `<strong>`, `<em>`, `<code>`, `<ul>`, `<table>` for clarity.
4. **Meaningful tags** — Tag by topic hierarchy: `python::decorators`, `biology::cell`.
5. **Avoid "yes/no" questions** — Rephrase to require recall: "What does X do?" not "Does X do Y?"
6. **Context in Front** — If ambiguous, add a small hint: `[Python]`, `[Biology]`, `[History]`.
7. **Images when possible** — Use `<img src="filename.png">` for diagrams (store via `anki-agent media store`).
