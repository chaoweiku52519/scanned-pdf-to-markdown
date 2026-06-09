---
name: scanned-pdf-to-markdown
description: Convert scanned image PDFs (no text layer) to structured Markdown via local OCR; spec-book profile for coding guidelines.
version: 1.0.0
homepage: https://github.com/chaoweiku52519/scanned-pdf-to-markdown
metadata: {"openclaw":{"requires":{"anyBins":["python","python3"]},"os":["win32","linux","darwin"],"emoji":"📄","homepage":"https://github.com/chaoweiku52519/scanned-pdf-to-markdown"}}
---

# Scanned PDF → Markdown

Convert **scanned image PDFs** (printer/scanner books, no text layer) into structured Markdown for specification documents (spec-book profile).

## When to use

- User asks to convert scanned PDF / OCR book / coding guideline to Markdown
- PDF has no extractable text layer (image-only pages)
- Documents with rule tags like `【1.1.1】`, `【级别】`, `【反例】`, `【正例】`

Do **not** use on PDFs with a text layer — use pdfminer or markitdown instead.

## Setup (once per environment)

Install Python dependencies:

```bash
python -m pip install -r {baseDir}/scripts/requirements.txt
```

Stack: `pypdfium2` (render), `rapidocr-onnxruntime` (OCR), `pdfminer.six` (text-layer detection).

## Output naming

Place outputs **next to the source PDF**:

| File | Rule |
|------|------|
| Final Markdown | `{pdf_stem}.md` — e.g. `开发规范1.pdf` → `开发规范1.md` |
| OCR raw (optional) | `{pdf_stem}.ocr-raw.txt` |

Do **not** append `_OCR`, page ranges, or other suffixes unless the user asks.

## Workflow

```text
- [ ] Step 1: Detect PDF type
- [ ] Step 2: OCR pages (script)
- [ ] Step 3: Structure into {pdf_stem}.md (agent)
- [ ] Step 4: Quality note (optional)
```

### Step 1: Detect PDF type

```bash
python {baseDir}/scripts/detect_pdf_type.py "path/to/file.pdf"
```

- **image-only** (0 chars/page) → continue with this skill
- **text-layer** → extract text directly; do not OCR

### Step 2: OCR pages

```bash
python {baseDir}/scripts/ocr_pages.py "path/to/file.pdf" --pages all --raw-out "path/to/file.ocr-raw.txt"
```

Options:

- `--pages`: `6-8`, `1,3,5`, or `all` (default `all`)
- `--scale`: default `3.5`
- `--min-confidence`: default `0.5`

Convert the user-requested page range directly; a trial subset is optional, not required.

### Step 3: Structure final Markdown

Read OCR raw output. Apply rules in `{baseDir}/profiles/spec-book.md`. Format reference: `{baseDir}/examples/dev-spec-p6-8.md`.

**Agent responsibilities** (scripts cannot do this reliably):

1. Remove headers/footers (book title, 3-digit page numbers)
2. Merge cross-page paragraphs and broken lines
3. Map structure: `# 第X章` / `## 1.1` / `### 【1.1.1】` / `**【级别】**` etc.
4. Format code blocks (`text` for trees, `xml`/`java` for snippets)
5. Fix high-confidence OCR typos in code only (`groupld`→`groupId`, `artifactld`→`artifactId`)
6. Mark scan illustrations as blockquotes
7. Do **not** infer content beyond the selected page range

Write result to `{pdf_stem}.md` beside the PDF.

### Step 4: Quality note (optional)

If code is present, append:

```markdown
<!--
ocr-quality:
  prose: high|medium
  code: review-required
  truncated: yes|no
-->
```

## Code handling

| Pattern | Action |
|---------|--------|
| Confidence ≥ 0.9 prose | Keep wording |
| Spacing/punctuation | Normalize |
| Known OCR code typo | Fix (`groupld`→`groupId`) |
| Ambiguous wording | Keep OCR literal or flag |
| Broken XML/Java tags | Fix obvious typos; flag rest |

Never present code as copy-paste-ready without review.

## Do not

- Use `markitdown` on image-only PDFs (returns empty)
- Auto-merge pages outside the requested range
- Rename output away from `{pdf_stem}.md` unless asked

## Quick example

User: `把 开发规范1.pdf 第6-8页转成 md`

```bash
python {baseDir}/scripts/detect_pdf_type.py "开发规范1.pdf"
python {baseDir}/scripts/ocr_pages.py "开发规范1.pdf" --pages 6-8 --raw-out "开发规范1.ocr-raw.txt"
```

Then produce `开发规范1.md` following `{baseDir}/profiles/spec-book.md`.

## Cursor IDE note

When installed at `.cursor/skills/scanned-pdf-to-markdown/`, treat `{baseDir}` as that folder path, or run scripts relative to the skill root.
