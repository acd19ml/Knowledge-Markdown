#!/usr/bin/env python3
from collections import Counter
import re
import sys
from pathlib import Path


CAPTION_PATTERNS = {
    "figure": re.compile(r"^\*\*Figure\s+(\d+)\.", re.M),
    "table": re.compile(r"^\*\*Table\s+(\d+)\.", re.M),
    "algorithm": re.compile(r"^\*\*Algorithm\s+(\d+)\.", re.M),
}

REF_PATTERNS = {
    "figure": re.compile(r"\bFigure\s+(\d+)\b"),
    "table": re.compile(r"\bTable\s+(\d+)\b"),
    "algorithm": re.compile(r"\bAlgorithm\s+(\d+)\b"),
}

LINK_REF_PATTERNS = {
    "figure": re.compile(r"\[([^\]]*?\d+(?:\.\d+)?[^\]]*?)\]\(#fig:[^)]+\)"),
    "table": re.compile(r"\[([^\]]*?\d+(?:\.\d+)?[^\]]*?)\]\(#tab:[^)]+\)"),
    "algorithm": re.compile(r"\[([^\]]*?\d+(?:\.\d+)?[^\]]*?)\]\(#alg:[^)]+\)"),
}

RESIDUE_PATTERNS = {
    "caption_residue": re.compile(r"^\*Caption:", re.M),
    "figure_dot": re.compile(r"\bFigure\.\s*\d+"),
    "table_dot": re.compile(r"\bTable\.\s*\d+"),
    "algorithm_dot": re.compile(r"\bAlgorithm\.\s*\d+"),
    "unresolved_label": re.compile(r"\[(?:fig|tab|alg|sec|subsec|eq):[^\]]+\]"),
    "html_table": re.compile(r"<table\b", re.I),
    "html_table_wrapper": re.compile(r'<div class="table\*">', re.I),
    "html_span": re.compile(r"<span\b", re.I),
    "html_figure": re.compile(r"<figure\b", re.I),
    "html_embed": re.compile(r"<embed\b", re.I),
    "duplicate_prefix": re.compile(r"\b(Figure|Table|Section|Appendix)\s+\1\b"),
}

ANCHOR_PATTERN = re.compile(r'<a id="([^"]+)"></a>')
LINK_TARGET_PATTERN = re.compile(r"\]\(#([^)]+)\)")


def caption_numbers(text: str, kind: str) -> list[int]:
    return sorted({int(x) for x in CAPTION_PATTERNS[kind].findall(text)})


def linked_reference_numbers(text: str, kind: str) -> list[int]:
    numbers: set[int] = set()
    for label in LINK_REF_PATTERNS[kind].findall(text):
        for match in re.findall(r"\d+", label):
            numbers.add(int(match))
    return sorted(numbers)


def prose_reference_numbers(text: str, kind: str) -> list[int]:
    stripped = CAPTION_PATTERNS[kind].sub("", text)
    prose = {int(x) for x in REF_PATTERNS[kind].findall(stripped)}
    linked = set(linked_reference_numbers(stripped, kind))
    return sorted(prose | linked)


def anchor_ids(text: str) -> list[str]:
    return ANCHOR_PATTERN.findall(text)


def link_targets(text: str) -> list[str]:
    return LINK_TARGET_PATTERN.findall(text)


def summarize_kind(text: str, kind: str) -> list[str]:
    refs = prose_reference_numbers(text, kind)
    captions = sorted({int(x) for x in CAPTION_PATTERNS[kind].findall(text)})
    missing_captions = [x for x in refs if x not in captions]
    unused_captions = [x for x in captions if x not in refs]

    lines = [
        f"{kind}: refs={refs or []}",
        f"{kind}: captions={captions or []}",
    ]
    if missing_captions:
        lines.append(f"{kind}: refs_without_caption={missing_captions}")
    if unused_captions:
        lines.append(f"{kind}: captions_without_ref={unused_captions}")
    return lines


def summarize_anchor_integrity(text: str) -> tuple[list[str], int]:
    anchors = anchor_ids(text)
    links = sorted(set(link_targets(text)))
    anchor_set = set(anchors)

    duplicate_anchors = sorted([key for key, value in Counter(anchors).items() if value > 1])
    missing_targets = [target for target in links if target not in anchor_set]
    unstable_anchors = sorted([anchor for anchor in anchor_set if anchor.strip() != anchor or " " in anchor])

    lines = [
        f"anchors: count={len(anchors)}",
        f"links: count={len(links)}",
    ]
    if duplicate_anchors:
        lines.append(f"anchors: duplicate_ids={duplicate_anchors}")
    if missing_targets:
        lines.append(f"anchors: missing_targets={missing_targets}")
    if unstable_anchors:
        lines.append(f"anchors: unstable_ids={unstable_anchors}")

    problems = len(duplicate_anchors) + len(missing_targets) + len(unstable_anchors)
    return lines, problems


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: audit_refs.py /absolute/path/to/paper.md", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")

    print(path)
    print()

    problems = 0

    for kind in ("figure", "table", "algorithm"):
        for line in summarize_kind(text, kind):
            print(line)
        print()

    anchor_lines, anchor_problems = summarize_anchor_integrity(text)
    for line in anchor_lines:
        print(line)
    print()
    problems += anchor_problems

    for name, pattern in RESIDUE_PATTERNS.items():
        matches = list(pattern.finditer(text))
        if matches:
            problems += len(matches)
            print(f"{name}: {len(matches)} match(es)")
            for m in matches[:10]:
                line_no = text.count("\n", 0, m.start()) + 1
                snippet = text[m.start(): text.find("\n", m.start())]
                print(f"  line {line_no}: {snippet}")
            if len(matches) > 10:
                print("  ...")

    for kind in ("figure", "table", "algorithm"):
        refs = prose_reference_numbers(text, kind)
        captions = caption_numbers(text, kind)
        problems += len([x for x in refs if x not in captions])
        problems += len([x for x in captions if x not in refs])

    if problems:
        print()
        print(f"audit: found {problems} potential issue(s)")
        return 1

    print("audit: no numbering mismatches, anchor integrity issues, duplicate prefixes, or HTML/label residue found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
