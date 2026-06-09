# scanned-pdf-to-markdown

Cursor Agent Skill：将**扫描版 PDF**（无文本层）通过本地 OCR 转为结构化 Markdown，适用于编码规范、架构规约等 spec-book 类文档。

## 特性

- 自动检测 PDF 是否有可提取文本层
- 本地 OCR（`pypdfium2` + `rapidocr-onnxruntime`），无需云端 API
- `spec-book` profile：识别 `【1.1.1】`、`【级别】`、`【反例】`、`【正例】` 等规范条目
- 输出命名：`开发规范1.pdf` → `开发规范1.md`

## 安装

### 1. 复制 Skill 到项目

```text
your-project/.cursor/skills/scanned-pdf-to-markdown/
```

或复制到个人 Skill 目录：

```text
~/.cursor/skills/scanned-pdf-to-markdown/
```

### 2. 安装 Python 依赖

```bash
python -m pip install -r .cursor/skills/scanned-pdf-to-markdown/scripts/requirements.txt
```

## 使用

在 Cursor 中对 Agent 说：

```text
用 scanned-pdf-to-markdown，把 开发规范1.pdf 转成 md
```

指定页码（可选）：

```text
用 scanned-pdf-to-markdown，把 开发规范1.pdf 第 6-8 页转成 md
```

### 手动运行脚本

```bash
# 检测 PDF 类型
python .cursor/skills/scanned-pdf-to-markdown/scripts/detect_pdf_type.py file.pdf

# OCR（默认全部页）
python .cursor/skills/scanned-pdf-to-markdown/scripts/ocr_pages.py file.pdf --raw-out file.ocr-raw.txt

# OCR 指定页
python .cursor/skills/scanned-pdf-to-markdown/scripts/ocr_pages.py file.pdf --pages 6-8
```

## 目录结构

```text
scanned-pdf-to-markdown/
├── SKILL.md                 # Agent 主流程
├── profiles/spec-book.md    # 规范书籍 profile
├── examples/dev-spec-p6-8.md
└── scripts/
    ├── detect_pdf_type.py
    ├── ocr_pages.py
    └── requirements.txt
```

## 工作流

```text
扫描 PDF → 类型检测 → 本地 OCR → Agent 结构化 → {原名}.md
```

脚本负责 OCR 认字；Agent 按 profile 整理章节、条目、代码块（与纯脚本相比质量更高）。

## 限制

- 适用于**扫描图像 PDF**，有文本层的 PDF 请直接用 pdfminer / markitdown
- 插图无法还原为原图，会以文字说明代替
- 代码块需人工复核后再复制使用
- 页码范围由用户指定；跨页条目不会自动从范围外补全

## License

MIT
