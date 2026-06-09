---
name: scanned-pdf-to-markdown
description: >-
  Converts scanned specification-book PDFs (image-only, no text layer) to structured
  Markdown using local OCR and spec-book formatting. Use when the user asks to convert
  scanned PDFs, OCR books, coding guidelines, or spec documents to Markdown, especially
  MetaSaaS/Huawei-style rule books with tags like 【1.1.1】【级别】【反例】【正例】.
---

# Scanned PDF → Markdown

Convert **scanned image PDFs** (printer/scanner books) into structured Markdown for specification documents.

## Scope

- **In scope**: spec-book profile (coding guidelines, architecture rules, 【条目】格式)
- **Out of scope**: PDFs with extractable text layer (use markitdown/pdfminer instead)
- **Goal**: usable structured Markdown draft, not pixel-perfect reproduction

## Output naming

Place outputs **next to the source PDF**:

| File | Rule |
|------|------|
| Final Markdown | `{pdf_stem}.md` — e.g. `开发规范1.pdf` → `开发规范1.md` |
| OCR raw (optional) | `{pdf_stem}.ocr-raw.txt` — confidence + text for review |

Do **not** append `_OCR`, `_规范正文`, page ranges, or other suffixes to the final `.md` unless the user explicitly asks.

## Dependencies

Install once (project or user environment):

```bash
python -m pip install -r .cursor/skills/scanned-pdf-to-markdown/scripts/requirements.txt
```

Stack: `pypdfium2` (render), `rapidocr-onnxruntime` (OCR), `pdfminer.six` (text-layer detection).

## Workflow

Copy and track:

```text
- [ ] Step 1: Detect PDF type
- [ ] Step 2: OCR pages (script)
- [ ] Step 3: Structure into {pdf_stem}.md (agent)
- [ ] Step 4: Brief quality note (optional)
```

### Step 1: Detect PDF type

```bash
python .cursor/skills/scanned-pdf-to-markdown/scripts/detect_pdf_type.py "path/to/file.pdf"
```

- If **image-only** (0 chars/page) → continue with this skill
- If **text layer exists** → do not OCR; extract text directly

### Step 2: OCR pages

```bash
python .cursor/skills/scanned-pdf-to-markdown/scripts/ocr_pages.py \
  "path/to/file.pdf" \
  --pages 1-55 \
  --raw-out "path/to/file.ocr-raw.txt"
```

- `--pages`: optional. Formats: `6-8`, `1,3,5`, `all` (default `all`)
- `--scale`: default `3.5` (raise for small text, lower for speed)
- `--min-confidence`: default `0.5`

The user may optionally request a subset first; if not specified, convert the requested or full range directly.

### Step 3: Structure final Markdown

Read OCR raw output and apply [profiles/spec-book.md](profiles/spec-book.md).

**Agent responsibilities** (scripts cannot do this reliably):

1. Remove headers/footers (book title, 3-digit page numbers)
2. Merge cross-page paragraphs and broken lines
3. Map structure:
   - `# 第X章 …` / `## 1.1 …` / `### 【1.1.1】…`
   - `**【级别】**` `**【描述】**` `**【反例】**` `**【正例】**` etc.
4. Format code blocks (`text` for directory trees, `xml`/`java` for snippets)
5. Fix high-confidence OCR typos in code only (`groupld`→`groupId`, `artifactld`→`artifactId`)
6. Mark illustrations as blockquotes when the source is a scan image
7. Do **not** infer missing content beyond the selected page range

Write result to `{pdf_stem}.md`.

### Step 4: Quality note (optional)

If code is present, append a short HTML comment block at the end:

```markdown
<!--
ocr-quality:
  prose: high|medium
  code: review-required
  truncated: yes|no — only if page range cuts mid-rule
-->
```

## Spec-book profile

Full rules: [profiles/spec-book.md](profiles/spec-book.md)

Golden example (format reference): [examples/dev-spec-p6-8.md](examples/dev-spec-p6-8.md)

## Code handling rules

| OCR pattern | Action | Tag |
|-------------|--------|-----|
| Confidence ≥ 0.9, prose | Keep wording | literal |
| Spacing/punctuation only | Normalize | normalized |
| Known OCR code typo (`groupld`) | Fix | inferred |
| Ambiguous word (e.g. 每一步/进一步) | Keep OCR literal OR flag | needs-review |
| XML/Java with broken tags | Fix obvious typos; flag rest | needs-review |

**Never** present code as copy-paste-ready without review.

## Do not

- Use `markitdown` on image-only scanned PDFs (returns empty)
- Auto-merge pages outside the user-requested range
- Rename output away from `{pdf_stem}.md` unless asked
- Over-engineer layout scripts; agent structuring is the quality step

## Quick example

User: `把 开发规范1.pdf 第6-8页转成 md`

```bash
python .cursor/skills/scanned-pdf-to-markdown/scripts/detect_pdf_type.py "开发规范1.pdf"
python .cursor/skills/scanned-pdf-to-markdown/scripts/ocr_pages.py "开发规范1.pdf" --pages 6-8 --raw-out "开发规范1.ocr-raw.txt"
```

Then produce `开发规范1.md` following the spec-book profile and golden example.
