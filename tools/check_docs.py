#!/usr/bin/env python3
"""Check the markdown docs in this repo so they do not rot.

Standard library only. Python 3.9 or later.

Checks, per markdown file:
  links      relative links resolve to an existing file or folder, and
             #anchors resolve to a heading or an explicit anchor.
  cross      links to github.com/PhysixSNET/<repo>/blob/main/<path> are
             cross-repo. They are verified when --root holds sibling
             checkouts (ROOT/<repo> or ROOT/apps/<repo>).
  mermaid    every ```mermaid block follows the house rules:
               - each label line is 26 characters or fewer;
               - no " · " lists;
               - at most 14 nodes;
               - classDef intended is declared if :::intended or -.-> is used;
               - node, edge and subgraph labels are quoted.
  coderef    `path:line` code refs in backticks that name an omegahive path
             exist in the --omegahive checkout, with lines in range.
             These are warnings only, because line numbers drift.

Exit status is 1 if there are errors, else 0.
Use --extract-mermaid DIR to write each mermaid block to DIR for rendering,
with DIR/index.tsv mapping each .mmd file to its source file and line.
"""

import argparse
import os
import re
import sys
from collections import defaultdict

ORG = "PhysixSNET"
MAX_LABEL = 26
MAX_NODES = 14
MAX_EDGES = 18  # the spec says "about 18"; a warning only

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".tox"}

FENCE_RE = re.compile(r"^( {0,3})(`{3,}|~{3,})\s*([^`\s]*)[^`]*$")
HEADING_RE = re.compile(r"^ {0,3}(#{1,6})\s+(.*?)\s*#*\s*$")
SETEXT_RE = re.compile(r"^ {0,3}(=+|-+)\s*$")
INLINE_CODE_RE = re.compile(r"(`+)(.+?)\1")
LINK_RE = re.compile(r"!?\[(?:[^\[\]]|\[[^\[\]]*\])*\]\(\s*(<[^>]*>|[^()\s]*(?:\([^()]*\)[^()\s]*)*)(?:\s+(?:\"[^\"]*\"|'[^']*'))?\s*\)")
REFDEF_RE = re.compile(r"^ {0,3}\[[^\]]+\]:\s*(<[^>]*>|\S+)")
HTML_LINK_RE = re.compile(r"""<(?:a|img)\b[^>]*?\b(?:href|src)\s*=\s*["']([^"']+)["']""", re.I)
HTML_ANCHOR_RE = re.compile(r"""<[a-z]+\b[^>]*?\b(?:name|id)\s*=\s*["']([^"']+)["']""", re.I)
GITHUB_RE = re.compile(
    r"^https?://github\.com/" + ORG + r"/([A-Za-z0-9_.\-]+)(?:/(blob|tree)/([^/#]+)(?:/([^#?]*))?)?/?(?:\?[^#]*)?(?:#(.*))?$"
)
CODEREF_RE = re.compile(
    r"^(?:omegahive/)?([A-Za-z0-9_.\-]+(?:/[A-Za-z0-9_.\-]+)+):(\d+(?:-\d+)?(?:,\s*\d+(?:-\d+)?)*)$"
)
LINE_ANCHOR_RE = re.compile(r"^L(\d+)(?:C\d+)?(?:-L(\d+)(?:C\d+)?)?$")


class Report:
    def __init__(self):
        self.items = []  # (level, rule, file, line, message)

    def add(self, level, rule, path, line, msg):
        self.items.append((level, rule, path, line, msg))

    def error(self, rule, path, line, msg):
        self.add("ERROR", rule, path, line, msg)

    def warn(self, rule, path, line, msg):
        self.add("WARNING", rule, path, line, msg)

    def info(self, rule, path, line, msg):
        self.add("INFO", rule, path, line, msg)

    def count(self, level):
        return sum(1 for i in self.items if i[0] == level)


# ---------------------------------------------------------------- markdown

def find_markdown(root):
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(filenames):
            if name.lower().endswith((".md", ".markdown")):
                out.append(os.path.join(dirpath, name))
    return out


def split_blocks(lines):
    """Yield ('text', lineno, line) and ('fence', start_lineno, info, body_lines)."""
    i = 0
    n = len(lines)
    while i < n:
        m = FENCE_RE.match(lines[i])
        if m:
            marker = m.group(2)
            info = m.group(3).lower()
            start = i + 1
            body = []
            i += 1
            closed = False
            while i < n:
                close = re.match(r"^ {0,3}(" + re.escape(marker[0]) + "{" + str(len(marker)) + r",})\s*$", lines[i])
                if close:
                    closed = True
                    break
                body.append(lines[i])
                i += 1
            yield ("fence", start, info, body, closed)
            i += 1
            continue
        yield ("text", i + 1, lines[i])
        i += 1


def strip_inline_code(text):
    return INLINE_CODE_RE.sub(lambda m: " " * len(m.group(0)), text)


def heading_text_to_slug(text):
    t = text
    t = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = t.replace("`", "")
    t = t.strip().lower()
    # GitHub keeps letters, numbers, spaces, hyphens and underscores.
    t = "".join(ch for ch in t if ch.isalnum() or ch in " -_")
    return t.replace(" ", "-")


def collect_anchors(lines):
    anchors = set()
    seen = defaultdict(int)
    prev = None
    for block in split_blocks(lines):
        if block[0] == "fence":
            prev = None
            continue
        _, _, line = block
        for m in HTML_ANCHOR_RE.finditer(line):
            anchors.add(m.group(1).lower())
        text = None
        m = HEADING_RE.match(line)
        if m:
            text = m.group(2)
        elif prev is not None and prev.strip() and SETEXT_RE.match(line) and not HEADING_RE.match(prev) \
                and not prev.lstrip().startswith(("|", "-", "*", ">")):
            text = prev.strip()
        if text is not None:
            base = heading_text_to_slug(text)
            k = seen[base]
            anchors.add(base if k == 0 else "%s-%d" % (base, k))
            seen[base] += 1
        prev = line
    return anchors


class Docs:
    """Caches file lines and anchors for any markdown file on disk."""

    def __init__(self):
        self._lines = {}
        self._anchors = {}

    def lines(self, path):
        path = os.path.realpath(path)
        if path not in self._lines:
            try:
                with open(path, encoding="utf-8", errors="replace") as fh:
                    self._lines[path] = fh.read().splitlines()
            except OSError:
                self._lines[path] = None
        return self._lines[path]

    def anchors(self, path):
        path = os.path.realpath(path)
        if path not in self._anchors:
            ls = self.lines(path)
            self._anchors[path] = collect_anchors(ls) if ls is not None else set()
        return self._anchors[path]


def check_anchor(docs, rep, rel, lineno, target_file, anchor, shown):
    if not anchor:
        return
    if os.path.isdir(target_file):
        return
    m = LINE_ANCHOR_RE.match(anchor)
    if m and (anchor.lower() not in docs.anchors(target_file)):
        ls = docs.lines(target_file)
        if ls is None:
            return
        hi = int(m.group(2) or m.group(1))
        if hi > len(ls):
            rep.error("links", rel, lineno, "%s: line %d is past the end (%d lines)" % (shown, hi, len(ls)))
        return
    if not target_file.lower().endswith((".md", ".markdown")):
        return
    if anchor.lower() not in docs.anchors(target_file):
        rep.error("links", rel, lineno, "%s: no heading or anchor '#%s'" % (shown, anchor))


def check_github_link(docs, rep, rel, lineno, url, root):
    m = GITHUB_RE.match(url)
    if not m:
        return
    repo, kind, branch, path, anchor = m.groups()
    if kind and branch != "main":
        rep.warn("cross", rel, lineno, "%s: links to branch '%s', not main" % (url, branch))
    if root is None:
        rep.info("cross", rel, lineno, "cross-repo link to %s (not verified; pass --root)" % (repo + ("/" + path if path else "")))
        return
    base = None
    for cand in (os.path.join(root, repo), os.path.join(root, "apps", repo)):
        if os.path.isdir(cand):
            base = cand
            break
    if base is None:
        rep.warn("cross", rel, lineno, "%s: no sibling checkout of '%s' under --root" % (url, repo))
        return
    if not path:
        return
    target = os.path.join(base, path.rstrip("/"))
    if not os.path.exists(target):
        rep.error("cross", rel, lineno, "%s: '%s' does not exist in %s" % (url, path, repo))
        return
    if kind == "blob" and os.path.isdir(target):
        rep.warn("cross", rel, lineno, "%s: is a folder; GitHub wants /tree/ not /blob/" % url)
    check_anchor(docs, rep, rel, lineno, target, anchor, url)


def check_links(docs, rep, repo_root, path, rel, lines, root):
    targets = []  # (lineno, target)
    for block in split_blocks(lines):
        if block[0] == "fence":
            continue
        _, lineno, line = block
        clean = strip_inline_code(line)
        for m in LINK_RE.finditer(clean):
            targets.append((lineno, m.group(1)))
        m = REFDEF_RE.match(clean)
        if m:
            targets.append((lineno, m.group(1)))
        for m in HTML_LINK_RE.finditer(clean):
            targets.append((lineno, m.group(1)))
    for lineno, target in targets:
        target = target.strip()
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1].strip()
        if not target:
            rep.error("links", rel, lineno, "empty link target")
            continue
        low = target.lower()
        if low.startswith(("http://", "https://")):
            check_github_link(docs, rep, rel, lineno, target, root)
            continue
        if re.match(r"^[a-z][a-z0-9+.\-]*:", low):  # mailto:, ftp:, etc.
            continue
        file_part, _, anchor = target.partition("#")
        file_part = file_part.split("?", 1)[0]
        file_part = re.sub(r"%20", " ", file_part)
        if file_part == "":
            check_anchor(docs, rep, rel, lineno, path, anchor, target)
            continue
        if file_part.startswith("/"):
            dest = os.path.join(repo_root, file_part.lstrip("/"))
        else:
            dest = os.path.join(os.path.dirname(path), file_part)
        dest = os.path.normpath(dest)
        if not os.path.realpath(dest).startswith(os.path.realpath(repo_root) + os.sep) \
                and os.path.realpath(dest) != os.path.realpath(repo_root):
            rep.error("links", rel, lineno, "%s: points outside this repo; use a github.com/%s link" % (target, ORG))
            continue
        if not os.path.exists(dest):
            rep.error("links", rel, lineno, "%s: file or folder does not exist" % target)
            continue
        check_anchor(docs, rep, rel, lineno, dest, anchor, target)


# ---------------------------------------------------------------- code refs

SHORT_REF_RE = re.compile(r"^([A-Za-z0-9_.\-]+\.[A-Za-z0-9]+)?:(\d+(?:-\d+)?(?:,\s*\d+(?:-\d+)?)*)$")


def check_coderefs(docs, rep, rel, lines, omegahive, stats):
    """Check `path:line` refs against the omegahive checkout (warnings only).

    Shorthand refs are resolved too:
      `STATUS.md:3` -> a top-level omegahive file, if one has that name;
      `name.py:12`  -> else the last full omegahive path in this file named name.py;
      `:12`         -> the last omegahive path on the same line.
    """
    if omegahive is None:
        return
    top = set(os.listdir(omegahive))
    by_base = {}
    for block in split_blocks(lines):
        if block[0] == "fence":
            continue
        _, lineno, line = block
        last_on_line = None
        for m in INLINE_CODE_RE.finditer(line):
            code = m.group(2).strip()
            cm = CODEREF_RE.match(code)
            if cm:
                ref_path, spec = cm.group(1), cm.group(2)
                if ref_path.split("/", 1)[0] not in top:
                    last_on_line = None
                    continue  # not an omegahive path (another repo)
                by_base[os.path.basename(ref_path)] = ref_path
            else:
                sm = SHORT_REF_RE.match(code)
                if not sm:
                    continue
                base, spec = sm.group(1), sm.group(2)
                if base and os.path.isfile(os.path.join(omegahive, base)):
                    ref_path = base  # a top-level file such as STATUS.md
                else:
                    ref_path = by_base.get(base) if base else last_on_line
                    if not ref_path:
                        continue
                    stats["shortrefs"] += 1
            last_on_line = ref_path
            stats["coderefs"] += 1
            full = os.path.join(omegahive, ref_path)
            shown = code if code.startswith(ref_path) or code.startswith("omegahive/") else "%s (%s)" % (code, ref_path)
            if not os.path.isfile(full):
                rep.warn("coderef", rel, lineno, "`%s`: '%s' not found in the omegahive checkout" % (shown, ref_path))
                continue
            ls = docs.lines(full)
            n = len(ls) if ls is not None else 0
            for part in spec.split(","):
                part = part.strip()
                lo, _, hi = part.partition("-")
                lo = int(lo)
                hi = int(hi) if hi else lo
                if lo < 1 or hi < lo:
                    rep.warn("coderef", rel, lineno, "`%s`: bad line range %s" % (shown, part))
                elif hi > n:
                    rep.warn("coderef", rel, lineno, "`%s`: line %d is past the end of %s (%d lines)" % (shown, hi, ref_path, n))


# ---------------------------------------------------------------- mermaid

QUOTED_RE = re.compile(r'"[^"]*"')
BR_RE = re.compile(r"<br\s*/?>", re.I)
TAG_RE = re.compile(r"</?([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>")
# Arrows: --> --- -.-> -.- ==> === --o --x <--> and longer variants.
ARROW_RE = re.compile(r"(?:<|(?<=\s)[ox])?(?:-{2,}|={2,}|-\.+-|~{3,})(?:>|[ox](?=\s|$))?")
FLOW_SKIP = ("classdef", "class ", "style ", "linkstyle", "click ", "direction ", "%%", "flowchart", "graph", "accTitle", "accDescr")
SEQ_ARROW_RE = re.compile(r"^\s*([A-Za-z0-9_]+)\s*(?:-{1,2}>>|-{1,2}>|-{1,2}x|-{1,2}\)|<<-{1,2}>>)[+\-]?\s*([A-Za-z0-9_]+)\s*:(.*)$")


def label_segments(text):
    return [s.strip() for s in BR_RE.split(text)]


def check_label_text(rep, rel, lineno, text, what):
    for seg in label_segments(text):
        if len(seg) > MAX_LABEL:
            rep.error("mermaid", rel, lineno, "%s line is %d characters (max %d): \"%s\"" % (what, len(seg), MAX_LABEL, seg))
    for m in TAG_RE.finditer(text):
        if m.group(1).lower() != "br":
            rep.warn("mermaid", rel, lineno, "HTML other than <br/> in a label: %s" % m.group(0))


def strip_brackets(s):
    """Remove bracketed label groups repeatedly; return (stripped, contents)."""
    contents = []
    pat = re.compile(r"\[[^\[\]]*\]|\([^()]*\)|\{[^{}]*\}")
    while True:
        found = pat.findall(s)
        if not found:
            break
        contents.extend(found)
        s = pat.sub(" ", s)
    return s, contents


def check_mermaid(rep, rel, start, body, stats, extract):
    stats["mermaid"] += 1
    text = "\n".join(body)
    lines = [(start + 1 + i, l) for i, l in enumerate(body)]
    meaningful = [(n, l.strip()) for n, l in lines if l.strip() and not l.strip().startswith("%%")]
    if not meaningful:
        rep.error("mermaid", rel, start, "empty mermaid block")
        return
    kind = meaningful[0][1].split()[0].lower()

    if extract is not None:
        safe = re.sub(r"[^A-Za-z0-9]+", "_", rel).strip("_")
        out = os.path.join(extract, "%s__L%d.mmd" % (safe, start))
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        with open(os.path.join(extract, "index.tsv"), "a", encoding="utf-8") as fh:
            fh.write("%s\t%s\t%d\n" % (os.path.basename(out), rel, start))

    for n, l in lines:
        if " · " in l:
            rep.error("mermaid", rel, n, "uses a ' · ' list; use commas or <br/>")

    uses_intended = (":::intended" in text) or re.search(r"-\.+->|-\.+-", text) or re.search(r"^\s*class\s+.*\bintended\b", text, re.M)
    if uses_intended and not re.search(r"^\s*classDef\s+intended\b", text, re.M):
        rep.error("mermaid", rel, start, "uses :::intended or -.-> but does not declare 'classDef intended'")

    if kind in ("flowchart", "graph"):
        check_flowchart(rep, rel, start, meaningful)
    elif kind == "sequencediagram":
        check_sequence(rep, rel, start, meaningful)
    else:
        for n, l in meaningful[1:]:
            for q in QUOTED_RE.findall(l):
                check_label_text(rep, rel, n, q[1:-1], "label")
        rep.info("mermaid", rel, start, "'%s' diagram: only generic rules checked" % kind)


def check_flowchart(rep, rel, start, meaningful):
    nodes = {}
    subgraphs = set()
    edges = 0
    for n, l in meaningful[1:]:
        low = l.lower()
        # Labels: every quoted string is a label.
        for q in QUOTED_RE.findall(l):
            check_label_text(rep, rel, n, q[1:-1], "label")
        if low.startswith(FLOW_SKIP) or low == "end":
            continue
        s = QUOTED_RE.sub("Q", l)
        if low.startswith("subgraph"):
            rest = s[len("subgraph"):].strip()
            m = re.match(r"^([A-Za-z0-9_\-]+)\s*(.*)$", rest)
            if m:
                subgraphs.add(m.group(1))
                tail = m.group(2).strip()
                if tail and not re.match(r"^\[\s*Q\s*\]$", tail):
                    rep.error("mermaid", rel, n, "subgraph title is not quoted; use subgraph id[\"Title\"]")
            elif rest != "Q":
                rep.error("mermaid", rel, n, "subgraph title is not quoted; use subgraph id[\"Title\"]")
            continue
        # Edge labels: |...| must be quoted; "-- text -->" must be quoted.
        for el in re.findall(r"\|([^|]*)\|", s):
            if el.strip() != "Q":
                rep.error("mermaid", rel, n, "edge label |%s| is not quoted; use |\"%s\"|" % (el, el.strip()))
        for el in re.findall(r"(?:^|\s)(?:--|==|-\.)\s+([^\s\-=.>|Q][^>|]*?)\s+(?:-->|==>|\.->|---)", s):
            rep.error("mermaid", rel, n, "edge label '%s' is not quoted" % el.strip())
        s = re.sub(r"(^|\s)(?:--|==|-\.)\s+[^\s\-=.>|][^>|]*?\s+(-->|==>|\.->|---)", r"\1 \2", s)
        s = re.sub(r"\|[^|]*\|", " ", s)
        s = re.sub(r":::[A-Za-z0-9_\-]+", " ", s)
        edges += len(ARROW_RE.findall(s))
        s = ARROW_RE.sub(" ", s)
        # Asymmetric shape: id>label]
        s = re.sub(r"(?<=[A-Za-z0-9_])>[^\]]*\]", lambda m: "[" + m.group(0)[1:], s)
        s, contents = strip_brackets(s)
        for c in contents:
            inner = c[1:-1].strip().strip("[](){}/\\>").strip()
            if inner and inner != "Q":
                rep.error("mermaid", rel, n, "node label %s is not quoted; use [\"...\"]" % c)
        for tok in re.findall(r"[A-Za-z0-9_]+", s.replace("&", " ")):
            if tok in ("Q",):
                continue
            nodes.setdefault(tok, n)
    for sg in subgraphs:
        nodes.pop(sg, None)
    if len(nodes) > MAX_NODES:
        rep.error("mermaid", rel, start, "%d nodes (max %d); split the diagram" % (len(nodes), MAX_NODES))
    if edges > MAX_EDGES:
        rep.warn("mermaid", rel, start, "%d edges (about %d max); consider splitting" % (edges, MAX_EDGES))


def check_sequence(rep, rel, start, meaningful):
    parts = set()
    for n, l in meaningful[1:]:
        m = re.match(r"^\s*(participant|actor)\s+([A-Za-z0-9_]+)(?:\s+as\s+(.*))?$", l)
        if m:
            parts.add(m.group(2))
            if m.group(3):
                check_label_text(rep, rel, n, m.group(3).strip().strip('"'), "participant")
            continue
        m = SEQ_ARROW_RE.match(l)
        if m:
            parts.add(m.group(1))
            parts.add(m.group(2))
            check_label_text(rep, rel, n, m.group(3).strip(), "message")
            continue
        m = re.match(r"^\s*(note\s+\w+(?:\s+of)?\s+[^:]+|loop|alt|else|opt|par|and|critical|break|rect)\s*:?\s*(.*)$", l, re.I)
        if m and m.group(2):
            check_label_text(rep, rel, n, m.group(2).strip(), "note")
    if len(parts) > MAX_NODES:
        rep.error("mermaid", rel, start, "%d participants (max %d); split the diagram" % (len(parts), MAX_NODES))


# ---------------------------------------------------------------- main

def main(argv=None):
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description="Check markdown links, mermaid house rules and code refs.")
    ap.add_argument("--repo", default=os.path.dirname(here), help="repo to check (default: the repo holding this script)")
    ap.add_argument("--omegahive", metavar="DIR", help="omegahive checkout for `path:line` code refs (warnings)")
    ap.add_argument("--root", metavar="DIR", help="folder of sibling checkouts, to verify cross-repo links")
    ap.add_argument("--extract-mermaid", metavar="DIR", help="write each mermaid block to DIR as .mmd")
    ap.add_argument("--quiet", action="store_true", help="hide INFO lines")
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = ap.parse_args(argv)

    repo = os.path.abspath(args.repo)
    omegahive = os.path.abspath(args.omegahive) if args.omegahive else None
    root = os.path.abspath(args.root) if args.root else None
    if omegahive and not os.path.isdir(omegahive):
        ap.error("--omegahive %s is not a folder" % omegahive)
    if root and not os.path.isdir(root):
        ap.error("--root %s is not a folder" % root)
    if args.extract_mermaid:
        os.makedirs(args.extract_mermaid, exist_ok=True)
        for name in os.listdir(args.extract_mermaid):
            if name.endswith(".mmd") or name == "index.tsv":
                os.remove(os.path.join(args.extract_mermaid, name))

    rep = Report()
    docs = Docs()
    stats = defaultdict(int)
    files = find_markdown(repo)
    for path in files:
        rel = os.path.relpath(path, repo)
        lines = docs.lines(path) or []
        stats["files"] += 1
        for block in split_blocks(lines):
            if block[0] == "fence":
                _, start, info, body, closed = block
                if not closed:
                    rep.error("markdown", rel, start, "code fence is never closed")
                if info == "mermaid":
                    check_mermaid(rep, rel, start, body, stats, args.extract_mermaid)
        check_links(docs, rep, repo, path, rel, lines, root)
        check_coderefs(docs, rep, rel, lines, omegahive, stats)

    order = {"ERROR": 0, "WARNING": 1, "INFO": 2}
    for level, rule, f, line, msg in sorted(rep.items, key=lambda i: (i[2], i[3], order[i[0]])):
        if level == "INFO" and args.quiet:
            continue
        print("%s:%d: %s [%s] %s" % (f, line, level, rule, msg))
    errors = rep.count("ERROR")
    warnings = rep.count("WARNING")
    print("\nchecked %d markdown files, %d mermaid blocks, %d omegahive code refs (%d shorthand)%s: %d errors, %d warnings"
          % (stats["files"], stats["mermaid"], stats["coderefs"], stats["shortrefs"],
             "" if omegahive else " (code refs skipped; pass --omegahive)", errors, warnings))
    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
