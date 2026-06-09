#!/usr/bin/env python3
"""OCR selected pages from a scanned PDF; write raw text with confidence scores."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import numpy as np
import pypdfium2 as pdfium
from rapidocr_onnxruntime import RapidOCR


def parse_pages(spec: str, total: int) -> list[int]:
    spec = spec.strip().lower()
    if spec in ("all", "*"):
        return list(range(total))

    pages: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_s, end_s = part.split("-", 1)
            start = int(start_s)
            end = int(end_s)
            if start < 1 or end < start:
                raise ValueError(f"invalid page range: {part}")
            for p in range(start, end + 1):
                if p > total:
                    raise ValueError(f"page {p} exceeds total pages ({total})")
                pages.add(p - 1)
        else:
            p = int(part)
            if p < 1 or p > total:
                raise ValueError(f"page {p} out of range 1-{total}")
            pages.add(p - 1)
    return sorted(pages)


def box_stats(box):
    xs = [pt[0] for pt in box]
    ys = [pt[1] for pt in box]
    return min(xs), min(ys), max(xs), max(ys)


def ocr_page(ocr, doc, page_index: int, scale: float, min_confidence: float):
    page = doc[page_index]
    image = page.render(scale=scale).to_pil().convert("RGB")
    result, _elapsed = ocr(np.array(image))
    rows = []
    if not result:
        return rows
    for item in result:
        box, text, score = item[0], item[1], float(item[2])
        text = re.sub(r"[ \t]+", " ", text.strip())
        if not text or score < min_confidence:
            continue
        x1, y1, x2, y2 = box_stats(box)
        rows.append({"text": text, "score": score, "x1": x1, "y1": y1, "x2": x2, "y2": y2})
    rows.sort(key=lambda r: (r["y1"], r["x1"]))
    return rows


def write_raw(out_path: Path, page_results: list[tuple[int, list[dict]]]) -> None:
    lines: list[str] = []
    for page_num, rows in page_results:
        lines.append(f"-- page {page_num} --")
        for row in rows:
            lines.append(f"{row['score']:.3f}\t{row['text']}")
        lines.append("")
    out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="OCR pages from a scanned PDF")
    parser.add_argument("pdf", type=Path, help="Input PDF path")
    parser.add_argument(
        "--pages",
        default="all",
        help='Page selection: "all", "6-8", "1,3,5" (1-based, default: all)',
    )
    parser.add_argument(
        "--raw-out",
        type=Path,
        default=None,
        help="Raw OCR output path (default: {pdf_stem}.ocr-raw.txt next to PDF)",
    )
    parser.add_argument("--scale", type=float, default=3.5, help="Render scale (default: 3.5)")
    parser.add_argument(
        "--min-confidence",
        type=float,
        default=0.5,
        help="Drop OCR lines below this confidence (default: 0.5)",
    )
    args = parser.parse_args()

    if not args.pdf.is_file():
        print(f"ERROR: file not found: {args.pdf}", file=sys.stderr)
        return 1

    raw_out = args.raw_out or args.pdf.with_suffix(".ocr-raw.txt")

    doc = pdfium.PdfDocument(str(args.pdf))
    total = len(doc)
    try:
        page_indices = parse_pages(args.pages, total)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    ocr = RapidOCR()
    page_results: list[tuple[int, list[dict]]] = []

    for idx in page_indices:
        print(f"OCR page {idx + 1}/{total} ...", flush=True)
        rows = ocr_page(ocr, doc, idx, args.scale, args.min_confidence)
        page_results.append((idx + 1, rows))

    write_raw(raw_out, page_results)
    print(f"pages_ocr={len(page_results)}")
    print(f"raw_out={raw_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
