#!/usr/bin/env python3
"""
OpenAtlas Bone Vocabulary → SKOS Turtle (Step 2)
Reads the JSON output from step 1 and emits a Skosmos-ready SKOS/Turtle file.

Python 3.11, mypy-friendly type hints, docstrings only, no inline comments.
URI scheme:
- ConceptScheme URI: BASE_URI
- Concept URIs: BASE_URI + "/concept/" + identifier
- Identifier: notation if present, else slug from Latin label; deduplicated by numeric suffixes
Labels:
- skos:prefLabel @la from Latin, @en and @de when present
- skos:notation from leading token like "T06"
Hierarchy:
- skos:broader to parent, skos:topConceptOf for roots, plus scheme's skos:hasTopConcept
Mappings:
- For each Anno/Wikidata/TA entry: skos:exactMatch unless marked "(close match)" → skos:closeMatch
- Non-URI mapping targets are serialized as string literals and recorded as warnings

Outputs:
- bonevoc.ttl: SKOS/Turtle
- bonevoc-ttl-issues.csv: warnings captured during export
"""

from __future__ import annotations

import csv
import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

BASE_URI: str = "https://vocabs.acdh.oeaw.ac.at/openatlas-bone"
SCHEME_TITLE: str = "OpenAtlas bone vocabulary"
INPUT_JSON: Path = Path("bonevoc-parse.json")
OUTPUT_TTL: Path = Path("bonevoc.ttl")
OUTPUT_ISSUES: Path = Path("bonevoc-ttl-issues.csv")

@dataclass
class ExternalRef:
    value: str
    close_match: bool

@dataclass
class Node:
    level: int
    label_la: str
    label_en: Optional[str]
    label_de: Optional[str]
    notation: Optional[str]
    anno: List[ExternalRef]
    wikidata: List[ExternalRef]
    ta: List[ExternalRef]
    warnings: List[str]
    children: List["Node"]
    raw_text: str = ""
    uri: Optional[str] = None
    slug: Optional[str] = None

def load_tree(path: Path) -> Tuple[str, str, List[Node]]:
    data: Dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    scheme_uri = str(data.get("scheme", {}).get("uri") or BASE_URI)
    scheme_title = str(data.get("scheme", {}).get("title") or SCHEME_TITLE)
    def build(node: Dict[str, Any]) -> Node:
        return Node(
            level=int(node.get("level", 0)),
            label_la=str(node.get("label_la") or ""),
            label_en=node.get("label_en"),
            label_de=node.get("label_de"),
            notation=node.get("notation"),
            anno=[ExternalRef(value=str(x["value"]), close_match=bool(x.get("close_match"))) for x in node.get("anno", [])],
            wikidata=[ExternalRef(value=str(x["value"]), close_match=bool(x.get("close_match"))) for x in node.get("wikidata", [])],
            ta=[ExternalRef(value=str(x["value"]), close_match=bool(x.get("close_match"))) for x in node.get("ta", [])],
            warnings=list(node.get("warnings", [])),
            children=[build(c) for c in node.get("children", [])],
            raw_text=str(node.get("raw_text") or ""),
        )
    roots = [build(n) for n in data.get("roots", [])]
    return scheme_uri, scheme_title, roots

def slugify(text: str) -> str:
    s = unicodedata.normalize("NFKD", text)
    s = s.encode("ascii", "ignore").decode("ascii")
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s or "concept"

def assign_uris(roots: Sequence[Node], base_uri: str) -> List[str]:
    issues: List[str] = []
    used: Dict[str, int] = {}
    def claim_slug(s: str) -> str:
        n = used.get(s, 0)
        if n == 0:
            used[s] = 1
            return s
        used[s] = n + 1
        return f"{s}-{n+1}"
    def traverse(n: Node, parent: Optional[Node]) -> None:
        pref = n.notation or slugify(n.label_la)
        n.slug = claim_slug(pref)
        n.uri = f"{base_uri}/concept/{n.slug}"
        for c in n.children:
            traverse(c, n)
    for r in roots:
        traverse(r, None)
    for k, v in used.items():
        if v > 1:
            issues.append(f"duplicate identifier base '{k}' assigned {v} variants")
    return issues

def is_uri(s: str) -> bool:
    return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", s))

def esc_lit(s: str) -> str:
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'

def lit_lang(s: str, lang: str) -> str:
    return f'{esc_lit(s)}@{lang}'

def triple(s: str, p: str, o: str) -> str:
    return f"{s} {p} {o} .\n"

def concept_block(n: Node, scheme_uri: str, issues: List[Tuple[str, str]]) -> str:
    if not n.uri:
        raise ValueError("URI not assigned")
    s = f"<{n.uri}>"
    lines: List[str] = []
    lines.append(triple(s, "a", "skos:Concept"))
    lines.append(triple(s, "skos:inScheme", f"<{scheme_uri}>"))
    lines.append(triple(s, "skos:prefLabel", lit_lang(n.label_la, "la")))
    if n.label_en:
        lines.append(triple(s, "skos:prefLabel", lit_lang(n.label_en, "en")))
    if n.label_de:
        lines.append(triple(s, "skos:prefLabel", lit_lang(n.label_de, "de")))
    if n.notation:
        lines.append(triple(s, "skos:notation", esc_lit(n.notation)))
    for field, lst in (("Anno", n.anno), ("Wikidata", n.wikidata), ("TA", n.ta)):
        for ref in lst:
            pred = "skos:closeMatch" if ref.close_match else "skos:exactMatch"
            if is_uri(ref.value):
                lines.append(triple(s, pred, f"<{ref.value}>"))
            else:
                lines.append(triple(s, pred, esc_lit(ref.value)))
                issues.append((n.uri, f"non-URI mapping in {field}: '{ref.value}'"))
    return "".join(lines)

def hierarchy_triples(roots: Sequence[Node], scheme_uri: str) -> str:
    lines: List[str] = []
    def visit(n: Node, parent: Optional[Node]) -> None:
        s = f"<{n.uri}>"
        if parent and parent.uri:
            lines.append(triple(s, "skos:broader", f"<{parent.uri}>"))
        else:
            lines.append(triple(s, "skos:topConceptOf", f"<{scheme_uri}>"))
            lines.append(triple(f"<{scheme_uri}>", "skos:hasTopConcept", s))
        for c in n.children:
            visit(c, n)
    for r in roots:
        visit(r, None)
    return "".join(lines)

def write_ttl(path: Path, scheme_uri: str, scheme_title: str, roots: Sequence[Node], issues: List[Tuple[str, str]]) -> None:
    head = []
    head.append("@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n")
    head.append("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n")
    head.append("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n")
    head.append("@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n")
    head.append(triple(f"<{scheme_uri}>", "a", "skos:ConceptScheme"))
    head.append(triple(f"<{scheme_uri}>", "rdfs:label", esc_lit(scheme_title)))
    body = []
    for n in iterate_nodes(roots):
        body.append(concept_block(n, scheme_uri, issues))
    body.append(hierarchy_triples(roots, scheme_uri))
    path.write_text("".join(head + body), encoding="utf-8")

def write_issues_csv(path: Path, issues: Sequence[Tuple[str, str]]) -> None:
    if not issues:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["concept_uri", "issue"])
        w.writerows(issues)

def iterate_nodes(roots: Sequence[Node]) -> Iterable[Node]:
    stack: List[Node] = list(roots)
    while stack:
        n = stack.pop(0)
        yield n
        stack[0:0] = n.children

def main() -> None:
    if not INPUT_JSON.exists():
        raise SystemExit(f"Input JSON not found: {INPUT_JSON}")
    scheme_uri, scheme_title, roots = load_tree(INPUT_JSON)
    assign_dup = assign_uris(roots, scheme_uri)
    issues: List[Tuple[str, str]] = []
    for msg in assign_dup:
        issues.append((scheme_uri, msg))
    write_ttl(OUTPUT_TTL, scheme_uri, scheme_title, roots, issues)
    write_issues_csv(OUTPUT_ISSUES, issues)
    print(f"Wrote {OUTPUT_TTL} with {len(list(iterate_nodes(roots)))} concepts")
    print(f"Issues: {len(issues)} → {OUTPUT_ISSUES}")

if __name__ == "__main__":
    main()
