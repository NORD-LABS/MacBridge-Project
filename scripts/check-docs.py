#!/usr/bin/env python3
"""Deterministic documentation checks for the MacBridge public repository.

Standard library only. Run from anywhere:  python3 scripts/check-docs.py

Checks:
  links      every relative link and image in Markdown (and HTML src/srcset/href) points to a file that exists
  anchors    every #fragment points to a heading that exists in the target file (GitHub slug rules)
  titles     every Markdown file has exactly one H1 (the root README may use a hero image instead),
             and no two files share the same H1
  svg        every SVG is well-formed XML, has a <title>, and declares role="img"
  mermaid    every mermaid block starts with a known diagram type and does not use a reserved node id
  media      every file in media/ is referenced somewhere (warning only: source assets may be kept)
  files      no unexpected binary types; no file above the size limit
  paths      no absolute local paths (/Users/, /home/, C:\\, file://)
  wording    no phrase from the project's banned list; no combined test count

Passing these checks does not prove how GitHub renders the pages. It only proves the sources are consistent.
"""
from __future__ import annotations

import os
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "node_modules"}
ALLOWED_BINARY = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico"}
TEXT_TYPES = {".md", ".svg", ".yml", ".yaml", ".py", ".txt", ".json", ".gitignore", ""}
MAX_BYTES = 1_000_000
MERMAID_TYPES = ("flowchart", "graph", "sequenceDiagram", "classDiagram", "stateDiagram", "stateDiagram-v2",
                 "erDiagram", "journey", "gantt", "pie", "timeline", "mindmap", "quadrantChart", "gitGraph")
MERMAID_RESERVED_IDS = {"end", "graph", "subgraph", "flowchart", "style", "class", "classDef", "click",
                        "linkStyle", "direction"}
BANNED = [
    "revolutioniz", "game-changing", "game changer", "cutting-edge", "unlock limitless", "limitless potential",
    "seamlessly bridg", "pushing the boundaries", "groundbreaking journey", "intersection of technology",
    "rapidly evolving", "digital landscape", "transforming the way", "it's not just", "it’s not just",
]
FORBIDDEN_CLAIMS = [
    (re.compile(r"\b873\b"), "combined test count (469 and 404 are different suites)"),
    (re.compile(r"\b\d{1,3}\s?% (complete|finished|done)\b", re.I), "completion percentage"),
]
LOCAL_PATH = re.compile(r"(/Users/[A-Za-z]|/home/[a-z]|[A-Z]:\\\\|file://)")

errors: list[str] = []
warnings: list[str] = []


def err(path: Path, msg: str, line: int | None = None) -> None:
    loc = str(path.relative_to(ROOT)) + (f":{line}" if line else "")
    errors.append(f"{loc}: {msg}")


def all_files() -> list[Path]:
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            out.append(Path(dirpath) / f)
    return sorted(out)


def strip_code(text: str) -> str:
    """Blank out fenced code blocks and inline code, keeping line numbers."""
    def blank(m: re.Match) -> str:
        return re.sub(r"[^\n]", " ", m.group(0))
    text = re.sub(r"^(```|~~~).*?^\1[ \t]*$", blank, text, flags=re.S | re.M)
    return re.sub(r"`[^`\n]*`", blank, text)


def slugify(heading: str) -> str:
    """GitHub's heading anchor rules: lowercase, drop punctuation, spaces become hyphens."""
    h = re.sub(r"<[^>]+>", "", heading)
    h = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", h)
    h = h.replace("`", "").strip().lower()
    out = []
    for ch in h:
        if ch in "-_ ":
            out.append("-" if ch == " " else ch)
        elif unicodedata.category(ch)[0] in "LN":
            out.append(ch)
    return "".join(out)


_anchor_cache: dict[Path, set[str]] = {}


def anchors_of(md: Path) -> set[str]:
    if md in _anchor_cache:
        return _anchor_cache[md]
    seen: dict[str, int] = {}
    result = set()
    for line in strip_code(md.read_text(encoding="utf-8")).splitlines():
        m = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if not m:
            continue
        base = slugify(m.group(2))
        n = seen.get(base, 0)
        seen[base] = n + 1
        result.add(base if n == 0 else f"{base}-{n}")
    for m in re.finditer(r'<a\s+(?:name|id)="([^"]+)"', md.read_text(encoding="utf-8")):
        result.add(m.group(1))
    _anchor_cache[md] = result
    return result


def check_target(src: Path, target: str, line: int) -> None:
    if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):  # http:, https:, mailto:
        return
    path_part, _, frag = target.partition("#")
    path_part = unquote(path_part)
    dest = src if not path_part else (src.parent / path_part).resolve()
    if path_part and not dest.exists():
        err(src, f"broken link: {target}", line)
        return
    if frag:
        if dest.is_dir() or dest.suffix.lower() != ".md":
            return
        if frag not in anchors_of(dest):
            err(src, f"missing anchor: {target}", line)


def check_markdown(md: Path, titles: dict[str, Path], referenced: set[Path]) -> None:
    raw = md.read_text(encoding="utf-8")
    text = strip_code(raw)
    lines = text.splitlines()
    for i, line in enumerate(lines, 1):
        for m in re.finditer(r"!?\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)", line):
            check_target(md, m.group(1), i)
            referenced.add((md.parent / unquote(m.group(1).split("#")[0])).resolve())
        for m in re.finditer(r'(?:src|href)="([^"]+)"', line):
            check_target(md, m.group(1), i)
            referenced.add((md.parent / unquote(m.group(1).split("#")[0])).resolve())
        for m in re.finditer(r'srcset="([^"]+)"', line):
            for part in m.group(1).split(","):
                url = part.strip().split()[0]
                check_target(md, url, i)
                referenced.add((md.parent / url).resolve())
    h1 = [l for l in lines if re.match(r"^# \S", l)]
    hero_readme = md == ROOT / "README.md" and not h1 and "<picture>" in raw
    if len(h1) != 1 and md.name != "LICENSE.md" and not hero_readme:
        err(md, f"expected exactly one H1, found {len(h1)}")
    elif h1:
        title = h1[0][2:].strip()
        if title in titles:
            err(md, f"duplicate title '{title}' (also {titles[title].relative_to(ROOT)})")
        titles[title] = md

    for block in re.finditer(r"^```mermaid\n(.*?)^```", raw, flags=re.S | re.M):
        body = block.group(1)
        line_no = raw[: block.start()].count("\n") + 1
        first = next((l.strip() for l in body.splitlines() if l.strip() and not l.strip().startswith("%%")), "")
        if not first.startswith(MERMAID_TYPES):
            err(md, f"mermaid block does not start with a diagram type: '{first}'", line_no)
        for m in re.finditer(r"(?:^|\s|-->|---)\s*([A-Za-z_][\w]*)\s*[\[\({]", body, flags=re.M):
            if m.group(1) in MERMAID_RESERVED_IDS:
                err(md, f"mermaid node id '{m.group(1)}' is a reserved word", line_no)
        if body.count("subgraph") != len(re.findall(r"^\s*end\s*$", body, flags=re.M)):
            err(md, "mermaid subgraph/end count mismatch", line_no)

    if md.name != "check-docs.py":
        low = text.lower()
        for phrase in BANNED:
            if phrase in low:
                err(md, f"banned phrase: '{phrase}'")
        for rx, why in FORBIDDEN_CLAIMS:
            for m in rx.finditer(text):
                err(md, f"forbidden claim ({why}): '{m.group(0)}'", text[: m.start()].count("\n") + 1)


def check_svg(svg: Path) -> None:
    try:
        root = ET.parse(svg).getroot()
    except ET.ParseError as e:
        err(svg, f"invalid XML: {e}")
        return
    ns = "{http://www.w3.org/2000/svg}"
    if root.tag != ns + "svg":
        err(svg, "root element is not <svg>")
    if root.find(ns + "title") is None:
        err(svg, "missing <title> (accessibility)")
    if root.get("role") != "img":
        err(svg, 'missing role="img"')
    if svg.read_text(encoding="utf-8").find("<script") >= 0:
        err(svg, "scripts are not allowed in SVG")


def main() -> int:
    files = all_files()
    titles: dict[str, Path] = {}
    referenced: set[Path] = set()
    for f in files:
        rel = f.relative_to(ROOT)
        ext = f.suffix.lower()
        size = f.stat().st_size
        if size > MAX_BYTES:
            err(f, f"file is {size} bytes (limit {MAX_BYTES})")
        if ext not in TEXT_TYPES and ext not in ALLOWED_BINARY:
            err(f, f"unexpected file type '{ext}'")
        if ext in {".md", ".svg", ".yml", ".yaml"}:
            content = f.read_text(encoding="utf-8")
            for i, line in enumerate(content.splitlines(), 1):
                if LOCAL_PATH.search(line):
                    err(f, "absolute local path", i)
        if ext == ".md":
            check_markdown(f, titles, referenced)
        elif ext == ".svg":
            check_svg(f)
        if rel.parts[0] == ".github" and ext in {".yml", ".yaml"}:
            if "\t" in f.read_text(encoding="utf-8"):
                err(f, "tab character in YAML")
    media = ROOT / "media"
    if media.is_dir():
        for asset in sorted(media.iterdir()):
            if asset.resolve() not in referenced:
                warnings.append(f"{asset.relative_to(ROOT)}: not referenced by any Markdown page (kept as a source asset?)")
    for w in warnings:
        print("warning: " + w)
    if errors:
        print("\n".join(errors))
        print(f"\n{len(errors)} problem(s).")
        return 1
    md_count = sum(1 for f in files if f.suffix == ".md")
    print(f"OK: {md_count} Markdown files, {len(titles)} titles, {len(_anchor_cache)} anchor tables checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
