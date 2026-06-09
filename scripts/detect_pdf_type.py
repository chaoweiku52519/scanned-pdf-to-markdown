#!/usr/bin/env python3
"""Detect whether a PDF has an extractable text layer or is image-only."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTChar, LTImage, LTFigure


def analyze_pdf(pdf_path: Path, sample_pages: int = 3) -> dict:
    total_chars = 0
    total_images = 0
    total_figures = 0
    pages_checked = 0

    for i, page_layout in enumerate(extract_pages(str(pdf_path))):
        if i >= sample_pages:
            break
        pages_checked += 1
        chars = images = figures = 0

        def walk(obj):
            nonlocal chars, images, figures
            if isinstance(obj, LTChar):
                chars += 1
            elif isinstance(obj, LTImage):
                images += 1
            elif isinstance(obj, LTFigure):
                figures += 1
            if hasattr(obj, "_objs"):
                for child in obj._objs:
                    walk(child)

        walk(page_layout)
        total_chars += chars
        total_images += images
        total_figures += figures

    if total_chars == 0:
        pdf_type = "image-only"
        recommendation = "Use scanned-pdf-to-markdown skill (OCR required)."
    elif total_chars < 50:
        pdf_type = "minimal-text"
        recommendation = "Mostly image; OCR likely still needed."
    else:
        pdf_type = "text-layer"
        recommendation = "Text extractable; use pdfminer/markitdown, not OCR."

    return {
        "path": str(pdf_path),
        "pages_checked": pages_checked,
        "chars": total_chars,
        "images": total_images,
        "figures": total_figures,
        "type": pdf_type,
        "recommendation": recommendation,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect PDF text layer vs image-only")
    parser.add_argument("pdf", type=Path, help="Path to PDF file")
    parser.add_argument(
        "--sample-pages",
        type=int,
        default=3,
        help="Number of leading pages to inspect (default: 3)",
    )
    args = parser.parse_args()

    if not args.pdf.is_file():
        print(f"ERROR: file not found: {args.pdf}", file=sys.stderr)
        return 1

    result = analyze_pdf(args.pdf, args.sample_pages)
    print(f"file:           {result['path']}")
    print(f"pages_checked:  {result['pages_checked']}")
    print(f"chars:          {result['chars']}")
    print(f"images:         {result['images']}")
    print(f"figures:        {result['figures']}")
    print(f"type:           {result['type']}")
    print(f"recommendation: {result['recommendation']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
