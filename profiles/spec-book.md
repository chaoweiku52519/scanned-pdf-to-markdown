# Spec-Book Profile

For scanned coding-guideline / architecture-spec books (e.g. MetaSaaS Java 开发规范).

## Document signals

- Rule IDs: `【1.1.1】`, `【2.3.4】`
- Meta tags: `【级别】`, `【描述】`, `【反例】`, `【正例】`, `【注意事项】`, `【例外】`, `【非DDD代码也适用】`, `【门禁支持情况】`
- Sections: `第N章`, `1.1`, `2.3 Java命名规范`
- Headers to strip: book title lines (e.g. `MetaSaaS Java开发规范`, `MetaSaaS5Java…`)
- Footers to strip: 3-digit page numbers (`002`, `003`)

## Markdown hierarchy

```markdown
# 第X章 章节标题

## 1.1 小节标题

### 【1.1.1】规则正文一句说完

**【级别】** 严重

**【描述】**

正文段落……

**【反例】**

1. 问题一……
2. 问题二……

```text
目录/包结构示意
```

**【正例】**

说明文字……

```xml
<!-- 或 java -->
```

**【注意事项】** …

**【例外】** …
```

## Paragraph rules

- Merge lines broken by OCR column width or page breaks
- Restore list items `1.` `2.` and bullet `·` / `-`
- Split English layer names: `PresentationLayer` → `Presentation Layer`
- Keep Chinese punctuation full-width where OCR captured it

## Header / footer removal

Remove when matched:

```regex
^MetaSaaS\s*Java
^MetaSaaS5?Java
^第[一二三四五六七八九十\d]+章\s*代码架构规范$   # repeated running headers
^\d{3}$                                         # page footer
```

Also drop lines in the bottom ~8% of page height if they are pure 3-digit numbers.

## Code blocks

### Directory / package trees (反例/正例)

Use `text` fence. Prefer tree form when OCR gives flat `.module` lines:

```text
com.mycompany.blog
├── .interfaces
│   ├── .article
│   └── pom.xml
```

Preserve OCR comments: `// 按照四层结构划分 maven 子模块`

### XML POM

- Fence: `xml`
- Fix high-confidence OCR: `groupld`→`groupId`, `artifactld`→`artifactId`, `projectxmlns`→`project xmlns`
- If page range truncates mid-tag, keep partial XML and add an HTML comment noting truncation
- Do not invent closing tags or dependency sections from memory

### Java

- Fence: `java`
- Fix spacing: `publicclass`→`public class`, `packagecom.`→`package com.`
- Flag low-confidence identifiers for review

## Illustrations

Scanned diagrams cannot be recovered as images. Replace with:

```markdown
> **示意**（原书为插图，OCR 识别文字如下）
> - 用户界面层
> - 应用层
```

## OCR fix table (code only)

| OCR | Corrected |
|-----|-----------|
| groupld | groupId |
| artifactld | artifactId |
| projectxmlns | project xmlns |
| starterl/ | starter// |
| Entityl | Entity |

Do **not** apply semantic fixes to prose without evidence (e.g. do not change 每一步→进一步 unless user confirms).

## Truncation

If the user selects a page range that cuts a rule mid-way:

- Include all content from selected pages
- Do not pull text from unselected pages
- Note truncation in an HTML comment at file end
