# scanned-pdf-to-markdown

Cursor Agent Skill / OpenClaw Skill：将**扫描版 PDF**（无文本层）通过本地 OCR 转为结构化 Markdown，适用于编码规范、架构规约等 spec-book 类文档。

## 安装

### ClawHub（OpenClaw，推荐）

```bash
clawhub install scanned-pdf-to-markdown
pip install -r ~/.openclaw/workspace/skills/scanned-pdf-to-markdown/scripts/requirements.txt
```

或从 GitHub 安装到 OpenClaw skills 目录：

```bash
git clone https://github.com/chaoweiku52519/scanned-pdf-to-markdown.git \
  ~/.openclaw/workspace/skills/scanned-pdf-to-markdown
pip install -r ~/.openclaw/workspace/skills/scanned-pdf-to-markdown/scripts/requirements.txt
openclaw skills list
```

使用：`/skill scanned-pdf-to-markdown` 或直接说「把 xxx.pdf 转成 md」。

### Cursor IDE

```text
your-project/.cursor/skills/scanned-pdf-to-markdown/
```

```bash
pip install -r .cursor/skills/scanned-pdf-to-markdown/scripts/requirements.txt
```

在 Cursor 中说：`用 scanned-pdf-to-markdown，把 xxx.pdf 转成 md`

> OpenClaw 版 SKILL.md 使用 `{baseDir}` 路径；Cursor 中将 `{baseDir}` 视为 skill 目录即可。

## 特性

- 自动检测 PDF 是否有可提取文本层
- 本地 OCR（`pypdfium2` + `rapidocr-onnxruntime`）
- `spec-book` profile：`【1.1.1】`、`【级别】`、`【反例】`、`【正例】`
- 输出命名：`开发规范1.pdf` → `开发规范1.md`

## 手动脚本

```bash
python scripts/detect_pdf_type.py file.pdf
python scripts/ocr_pages.py file.pdf --pages 6-8 --raw-out file.ocr-raw.txt
```

## 发布到 ClawHub

```bash
clawhub login
clawhub skill publish . --slug scanned-pdf-to-markdown --version 1.0.0 --changelog "Initial release"
```

## 目录结构

```text
scanned-pdf-to-markdown/
├── SKILL.md
├── profiles/spec-book.md
├── examples/dev-spec-p6-8.md
└── scripts/
    ├── detect_pdf_type.py
    ├── ocr_pages.py
    └── requirements.txt
```

## License

MIT
