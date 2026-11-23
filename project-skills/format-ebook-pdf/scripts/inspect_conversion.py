#!/usr/bin/env python3
"""Inspect a DOCX conversion; optionally compare table cells with a PDF.

The DOCX inspection uses the standard library. --pdf additionally requires
pdfplumber. Unverified cells require visual inspection; they are not necessarily
missing, since PDF table detection can fail on borderless or complex tables.
"""
import argparse
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
NS = {"w": W[1:-1]}


def text(node):
    return " ".join(t.text or "" for t in node.iter(W + "t"))


def normalize(value):
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", value or "")).replace("\u00ad", "")


def inspect(docx, pdf=None):
    with ZipFile(docx) as archive:
        document = ET.fromstring(archive.read("word/document.xml"))
        images = [n for n in archive.namelist() if n.startswith("word/media/")]
    tables = []
    cells = []
    for index, table in enumerate(document.iter(W + "tbl")):
        rows = table.findall(W + "tr")
        extracted = [[text(cell).strip() for cell in row.findall(W + "tc")] for row in rows]
        widths = [node.get(W + "w") for node in table.findall("w:tblGrid/w:gridCol", NS)]
        table_width = table.find("w:tblPr/w:tblW", NS)
        tables.append({
            "index": index, "rows": extracted, "grid_widths_twips": widths,
            "table_width": {key.split("}")[-1]: val for key, val in table_width.attrib.items()} if table_width is not None else None,
            "width_needs_review": not widths or any(not value or int(value) <= 0 for value in widths),
        })
        for row_index, row in enumerate(extracted):
            for col_index, content in enumerate(row):
                if content:
                    cells.append({"table": index, "row": row_index, "column": col_index, "text": content})
    markers = [text(p).strip() for p in document.iter(W + "p")
               if re.fullmatch(r"\s*(?:\[\d+\]\s*)+", text(p))]
    superscripts = sum(1 for link in document.iter(W + "hyperlink")
                       if re.fullmatch(r"\[(?:\d+|→)\]", text(link).strip())
                       and link.find('.//w:vertAlign[@w:val="superscript"]', NS) is not None)
    report = {
        "docx": str(Path(docx).resolve()), "media_parts": len(images),
        "bookmark_count": len(list(document.iter(W + "bookmarkStart"))),
        "hyperlink_count": len(list(document.iter(W + "hyperlink"))),
        "standalone_reference_paragraphs": markers,
        "superscript_citation_links": superscripts, "tables": tables,
    }
    if pdf:
        try:
            import pdfplumber
        except ImportError as exc:
            raise SystemExit("--pdf requires pdfplumber in the selected Python runtime") from exc
        rendered_cells = set()
        sizes = Counter()
        with pdfplumber.open(pdf) as rendered:
            for page in rendered.pages:
                for char in page.chars:
                    sizes[(char.get("fontname", ""), round(char["size"], 2))] += 1
                for table in page.find_tables():
                    for row in table.extract():
                        rendered_cells.update(normalize(cell) for cell in row if cell)
            report["pdf"] = {
                "path": str(Path(pdf).resolve()), "page_count": len(rendered.pages),
                "source_nonempty_cells": len(cells),
                "verified_cell_count": sum(normalize(c["text"]) in rendered_cells for c in cells),
                "unverified_cells": [c for c in cells if normalize(c["text"]) not in rendered_cells],
                "rendered_font_sizes": [{"font": f, "pt": pt, "characters": count}
                                        for (f, pt), count in sizes.most_common()],
                "note": "Unverified cells require geometric or visual review. This is not a complete layout or link validation.",
            }
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docx", type=Path)
    parser.add_argument("--pdf", type=Path)
    parser.add_argument("--out", type=Path, help="Write JSON report here instead of stdout")
    args = parser.parse_args()
    output = json.dumps(inspect(args.docx, args.pdf), ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.write_text(output, encoding="utf-8")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
