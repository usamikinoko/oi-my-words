#!/usr/bin/env python3
"""Mechanical metrics for one Markdown article (Chinese tech-blog oriented).

The metrics mirror the design notes in docs/ROADMAP.md so the four arms of a
case (A baseline / B generic instruction / C this skill / D human) can be
compared numerically instead of by impression alone.

Usage:
    python docs/tools/metrics.py docs/cases/<case-id>/C-skill.md
    python docs/tools/metrics.py <article.md> -o <case-id>/metrics.json
    python docs/tools/metrics.py <article.md> --table

Stdlib only, no third-party dependencies.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

CJK = "\u4e00-\u9fff"

FENCED_CODE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE = re.compile(r"`[^`]*`")
LINK_URL = re.compile(r"\]\([^)]*\)")
HEADING = re.compile(r"^\s{0,3}#{1,6}\s+")
LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
BLOCKQUOTE = re.compile(r"^\s*>")
SENTENCE_SPLIT = re.compile(r"[。！？!?…]+")
DASH = re.compile(r"——|—|–")
COLON = re.compile(r"：")
TERM_ANNOTATION = re.compile(r"[A-Za-z][A-Za-z0-9 .+\-_/]*（[" + CJK + r"]+）")

# Fixed connectives the guidelines ask writers to vary.
CONNECTIVES = ["首先", "然后", "其次", "综上", "总而言之", "总之", "最后", "因此", "然而", "此外", "另外"]

TABLE_KEYS = [
    "char_count",
    "paragraph_count",
    "paragraph_len_stdev",
    "sentence_count",
    "sentence_len_mean",
    "sentence_len_variance",
    "list_line_ratio",
    "dash_count",
    "colon_count",
    "term_annotation_count",
    "connective_total",
]


def strip_code(text: str) -> str:
    return INLINE_CODE.sub("", FENCED_CODE.sub("", text))


def analyse(text: str) -> dict:
    prose = LINK_URL.sub("", strip_code(text))
    lines = prose.splitlines()
    non_empty = [ln for ln in lines if ln.strip()]
    list_lines = [ln for ln in non_empty if LIST_ITEM.match(ln)]
    quote_lines = [ln for ln in non_empty if BLOCKQUOTE.match(ln)]
    heading_lines = [ln for ln in non_empty if HEADING.match(ln)]

    # Paragraphs: blank-line-separated blocks that are not headings / lists / quotes.
    blocks: list[str] = []
    buf: list[str] = []
    for ln in lines + [""]:
        if ln.strip() == "":
            if buf:
                blocks.append("\n".join(buf))
                buf = []
        else:
            buf.append(ln)
    paragraphs = [
        b
        for b in blocks
        if not (
            HEADING.match(b.splitlines()[0])
            or LIST_ITEM.match(b.splitlines()[0])
            or BLOCKQUOTE.match(b.splitlines()[0])
        )
    ]
    para_chars = [len(re.sub(r"\s", "", p)) for p in paragraphs]

    sentences = [
        s for s in SENTENCE_SPLIT.split(prose) if re.search(r"[" + CJK + r"A-Za-z0-9]", s)
    ]
    sent_chars = [len(re.sub(r"\s", "", s)) for s in sentences]

    connectives = {w: prose.count(w) for w in CONNECTIVES}
    connective_nonzero = {k: v for k, v in connectives.items() if v}

    return {
        "char_count": len(re.sub(r"\s", "", strip_code(text))),
        "line_count_non_empty": len(non_empty),
        "paragraph_count": len(paragraphs),
        "paragraph_char_lengths": para_chars,
        "paragraph_len_mean": round(statistics.mean(para_chars), 1) if para_chars else 0.0,
        "paragraph_len_stdev": round(statistics.pstdev(para_chars), 1) if len(para_chars) > 1 else 0.0,
        "sentence_count": len(sentences),
        "sentence_len_mean": round(statistics.mean(sent_chars), 1) if sent_chars else 0.0,
        "sentence_len_variance": round(statistics.pvariance(sent_chars), 1) if len(sent_chars) > 1 else 0.0,
        "heading_count": len(heading_lines),
        "list_line_count": len(list_lines),
        "list_line_ratio": round(len(list_lines) / len(non_empty), 3) if non_empty else 0.0,
        "blockquote_line_count": len(quote_lines),
        "dash_count": len(DASH.findall(prose)),
        "colon_count": len(COLON.findall(prose)),
        "term_annotation_count": len(TERM_ANNOTATION.findall(prose)),
        "connective_counts": connectives,
        "connective_total": sum(connectives.values()),
        "connective_nonzero": connective_nonzero,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Mechanical metrics for one Markdown article.")
    ap.add_argument("path", type=Path)
    ap.add_argument("-o", "--output", type=Path, default=None)
    ap.add_argument("--table", action="store_true", help="also print a Markdown summary table")
    args = ap.parse_args(argv)

    text = args.path.read_text(encoding="utf-8")
    result = {"file": args.path.name}
    result.update(analyse(text))

    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(payload)

    if args.table:
        print()
        print("| metric | value |")
        print("|---|---|")
        for key in TABLE_KEYS:
            print(f"| {key} | {result[key]} |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
