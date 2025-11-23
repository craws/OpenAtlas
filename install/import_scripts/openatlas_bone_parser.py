#!/usr/bin/env python3
"""
OpenAtlas Bone Vocabulary Parser (Step 1: Parse hierarchy from .docx)
Python 3.11, uses `python-docx` (import as `docx`) at runtime.

Robustly parses entries of the form:
  Latin [may contain (...) itself]
  (EN, DE; Anno: ...; Wikidata: ...; Terminologia Anatomica: ...)

Key fixes:
- Keeps parentheses that belong to the Latin label.
- Extracts only the final metadata block in trailing parentheses when it
  contains expected keys or the EN, DE pair.
- Works with embedded DOCX hyperlinks (expands to URLs).

Outputs:
- JSON tree with nodes and warnings
- CSV of issues
"""

from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

from docx import Document  # type: ignore
from docx.text.paragraph import Paragraph  # type: ignore

BASE_URI: str = "https://vocabs.acdh.oeaw.ac.at/openatlas-bone"
SCHEME_TITLE: str = "OpenAtlas bone vocabulary"
OUTPUT_JSON: Path = Path("bonevoc-parse.json")
OUTPUT_CSV: Path = Path("bonevoc-issues.csv")
FILE_PATH: Path = Path(
    "/home/bkoschicek/www/openatlas/files/openatlas_bone_voc_parse.docx")

_TA_STRICT_RE = re.compile(r"^A\d{2}\.\d{1,2}\.\d{2}\.\d{2,3}$")
_TA_LOOSE_RE = re.compile(r"A\d{2}\.\d{1,2}\.\d{2}\.\d{2,3}")
_URL_RE = re.compile(r"https?://\S+")
_QID_RE = re.compile(r"^Q\d+$")
_NOTATION_RE = re.compile(r"^\s*([A-Za-z0-9]{1,5})\s*-\s*(.+)$")

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}


@dataclass
class ExternalRef:
    value: str
    close_match: bool = False


@dataclass
class Node:
    level: int
    label_la: str
    label_en: Optional[str]
    label_de: Optional[str]
    notation: Optional[str] = None
    anno: List[ExternalRef] = field(default_factory=list)
    wikidata: List[ExternalRef] = field(default_factory=list)
    ta: List[ExternalRef] = field(default_factory=list)
    raw_text: str = ""
    warnings: List[str] = field(default_factory=list)
    children: List["Node"] = field(default_factory=list)


@dataclass
class ParseResult:
    roots: List[Node]
    warnings: List[str] = field(default_factory=list)


def normalize_space(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip())


def paragraph_text_with_hyperlinks(p: Paragraph) -> str:
    from docx.oxml.ns import qn  # type: ignore
    pieces: List[str] = []
    for child in p._p:  # type: ignore[attr-defined]
        if child.tag == qn("w:hyperlink"):
            rid = child.get(qn("r:id"))
            target = ""
            if rid and rid in p.part.rels:  # type: ignore[attr-defined]
                target = p.part.rels[rid].target_ref  # type: ignore[index]
            if target:
                pieces.append(target)
            else:
                texts = [t.text or "" for t in child.findall(".//w:t", NS)]
                pieces.append("".join(texts))
        else:
            texts = [t.text or "" for t in child.findall(".//w:t", NS)]
            pieces.append("".join(texts))
    return normalize_space("".join(pieces))


def extract_list_level(p: Paragraph) -> Optional[int]:
    try:
        pPr = p._p.pPr  # type: ignore[attr-defined]
        if pPr is None:
            return None
        numPr = pPr.numPr
        if numPr is None:
            return None
        ilvl = numPr.ilvl
        if ilvl is None:
            return 0
        return int(ilvl.val)  # type: ignore[arg-type]
    except Exception:
        return None


def fallback_level_from_indent(p: Paragraph) -> Optional[int]:
    try:
        left = p.paragraph_format.left_indent
        if left is None:
            return None
        twips = int(left)  # type: ignore[arg-type]
        return max(0, twips // 360)
    except Exception:
        return None


def find_trailing_metadata_block(text: str) -> Optional[Tuple[int, int, str]]:
    s = text.rstrip()
    if not s.endswith(")"):
        return None
    depth = 0
    for i in range(len(s) - 1, -1, -1):
        ch = s[i]
        if ch == ")":
            depth += 1
        elif ch == "(":
            depth -= 1
            if depth == 0:
                start = i
                end = len(s) - 1
                content = s[start + 1: end]
                if looks_like_metadata(content):
                    return start, end, content
                return None
    return None


def looks_like_metadata(content: str) -> bool:
    c = content.strip()
    if "Anno:" in c or "Wikidata:" in c or "Terminologia" in c:
        return True
    if ";" in c and "," in c:
        return True
    return False


def is_effective_bullet(p: Paragraph) -> bool:
    if extract_list_level(p) is not None:
        return True
    expanded = paragraph_text_with_hyperlinks(p)
    return find_trailing_metadata_block(expanded) is not None


def split_head_and_parens(text: str) -> Tuple[str, Optional[str]]:
    m = find_trailing_metadata_block(text)
    if not m:
        return normalize_space(text), None
    start, end, content = m
    head = normalize_space(text[:start].rstrip(" -—"))
    return head, normalize_space(content)


def parse_refs(
        field_value: str,
        kind: str,
        warn: List[str]) -> List[ExternalRef]:
    if field_value.strip() == "-":
        return []
    tokens: List[ExternalRef] = []
    parts = re.split(r"\s*[;,]\s*", field_value.strip())
    for part in parts:
        if not part:
            continue
        m = re.match(r"(\S+?)(?:\s*\((close match)\))?$", part)
        if not m:
            warn.append(f"{kind}: unrecognized token '{part}'")
            continue
        val = m.group(1)
        close = bool(m.group(2))
        if kind == "TA":
            if not _TA_STRICT_RE.match(val):
                if _TA_LOOSE_RE.search(val):
                    warn.append(
                        f"TA: non-standard code '{val}' "
                        "normalized expected like A00.0.00.000")
                else:
                    warn.append(f"TA: invalid code '{val}'")
        elif kind == "Wikidata":
            if _QID_RE.match(val):
                val = f"https://www.wikidata.org/wiki/{val}"
            if not _URL_RE.match(val):
                warn.append(f"Wikidata: invalid value '{val}'")
        elif kind == "Anno":
            if not _URL_RE.match(val):
                warn.append(f"Anno: invalid URL '{val}'")
        tokens.append(ExternalRef(value=val, close_match=close))
    return tokens


def parse_paren_block(
        content: str,
        warn: List[str]) -> \
            Tuple[Optional[str], Optional[str], Dict[str, List[ExternalRef]]]:
    parts = [normalize_space(x) for x in content.split(";")]
    if not parts:
        warn.append("missing parenthetical content")
        return None, None, {}
    first = parts[0] if parts else ""
    en, de = None, None
    if "," in first:
        a, b = first.split(",", 1)
        en, de = normalize_space(a), normalize_space(b)
    else:
        warn.append("missing EN, DE pair before semicolon")
    fields: Dict[str, List[ExternalRef]] = {
        "Anno": [],
        "Wikidata": [],
        "TA": []}
    for chunk in parts[1:]:
        if ":" not in chunk:
            warn.append(f"missing ':' in field '{chunk}'")
            continue
        key, val = chunk.split(":", 1)
        key = normalize_space(key)
        val = normalize_space(val)
        if key.lower().startswith("anno"):
            fields["Anno"] = parse_refs(val, "Anno", warn)
        elif key.lower().startswith("wikidata"):
            fields["Wikidata"] = parse_refs(val, "Wikidata", warn)
        elif key.lower().startswith("terminologia"):
            fields["TA"] = parse_refs(val, "TA", warn)
        else:
            warn.append(f"unknown field '{key}'")
    return en, de, fields


def parse_line(text: str) -> Node:
    warnings: List[str] = []
    t = normalize_space(text)
    notation: Optional[str] = None
    m_not = _NOTATION_RE.match(t)
    if m_not:
        notation = m_not.group(1)
        t = normalize_space(m_not.group(2))
    head, par = split_head_and_parens(t)
    label_la = head
    label_en: Optional[str] = None
    label_de: Optional[str] = None
    anno: List[ExternalRef] = []
    wikidata: List[ExternalRef] = []
    ta: List[ExternalRef] = []
    if par:
        label_en, label_de, fields = parse_paren_block(par, warnings)
        anno = fields.get("Anno", [])
        wikidata = fields.get("Wikidata", [])
        ta = fields.get("TA", [])
    else:
        warnings.append("missing parenthetical metadata")
    return Node(
        level=0,
        label_la=label_la,
        label_en=label_en,
        label_de=label_de,
        notation=notation,
        anno=anno,
        wikidata=wikidata,
        ta=ta,
        raw_text=text,
        warnings=warnings,
    )


def build_tree(doc: Document) -> ParseResult:
    roots: List[Node] = []
    stack: List[Tuple[int, Node]] = []
    global_warn: List[str] = []
    for p in doc.paragraphs:
        if not is_effective_bullet(p):
            continue
        level = extract_list_level(p)
        if level is None:
            level = fallback_level_from_indent(p) or 0
        expanded = paragraph_text_with_hyperlinks(p)
        node = parse_line(expanded)
        node.level = level
        node.raw_text = p.text
        if not stack:
            roots.append(node)
            stack = [(level, node)]
            continue
        while stack and level <= stack[-1][0]:
            stack.pop()
        if not stack:
            roots.append(node)
            stack = [(level, node)]
        else:
            parent = stack[-1][1]
            parent.children.append(node)
            stack.append((level, node))
    return ParseResult(roots=roots, warnings=global_warn)


def flatten_issues(nodes: Sequence[Node]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    def visit(n: Node, path: List[str]) -> None:
        here = " / ".join(path + [n.label_la])
        for w in n.warnings:
            rows.append({"path": here, "warning": w, "raw": n.raw_text})
        for c in n.children:
            visit(c, path + [n.label_la])
    for r in nodes:
        visit(r, [])
    return rows


def to_json(result: ParseResult) -> str:
    def encode(node: Node) -> Dict[str, Any]:
        return {
            "level": node.level,
            "label_la": node.label_la,
            "label_en": node.label_en,
            "label_de": node.label_de,
            "notation": node.notation,
            "anno": [asdict(x) for x in node.anno],
            "wikidata": [asdict(x) for x in node.wikidata],
            "ta": [asdict(x) for x in node.ta],
            "raw_text": node.raw_text,
            "warnings": list(node.warnings),
            "children": [encode(c) for c in node.children],
        }
    payload = {
        "scheme": {"uri": BASE_URI, "title": SCHEME_TITLE},
        "roots": [encode(r) for r in result.roots],
        "warnings": result.warnings,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def write_json(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def write_issues_csv(path: Path, rows: Sequence[Dict[str, str]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["path", "warning", "raw"])
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    if not FILE_PATH.exists():
        raise SystemExit(f"Input DOCX not found: {FILE_PATH}")
    doc = Document(FILE_PATH)
    result = build_tree(doc)
    write_json(OUTPUT_JSON, to_json(result))
    issues = flatten_issues(result.roots)
    write_issues_csv(OUTPUT_CSV, issues)
    print(f"Parsed nodes (roots): {len(result.roots)}")
    print(f"Issues: {len(issues)}")
    print(f"Wrote: {OUTPUT_JSON} and {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
