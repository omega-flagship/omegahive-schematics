# Contributing to the schematics

This repo describes the OmegaHive code. It holds no code of its own, so the work is keeping pages accurate and diagrams readable. Read [`README.md`](README.md) and [`LEGEND.md`](LEGEND.md) first.

## Add a page
1. **Pick the section.** Put the page in the numbered folder it belongs to (for example `03-minds/`). Name it `NN-short-name.md`, numbered after the pages already there. A component card goes in `components/`.
2. **Use the page shape.** Copy the headings of a finished page in the same section: what it is, the diagrams, how it works, the intended shape, seams and contracts, how to plug in (only where relevant), what reviewers check, and references.
3. **Name the base commit.** Say near the top which `omegahive` commit the `path:line` refs point at.
4. **Cite what you read.** Every claim about current behaviour carries a `path:line` you actually read, in backticks, for example `hive/core/budgets.py:294`. Intended things cite where the intent is written down. Never present intended as built.
5. **Link, don't repeat.** If another page already explains something, link to it. Each fact lives in one place.
6. **Add it to the index.** List the page in its section's index and, for a new section, in [`README.md`](README.md).

## Links
- **Inside this repo:** relative links, for example `[Budgets](../05-governance/02-budgets-and-spend.md)`. Anchors follow GitHub's heading rules: lower case, spaces become `-`, punctuation dropped.
- **Other repos:** full links of the form `https://github.com/PhysixSNET/<repo>/blob/main/<path>` (use `/tree/main/` for a folder).
- **Code refs:** `path:line` or `path:start-end` in backticks, against the `omegahive` repo unless the page names another repo. Shorthand works on the same line or after the full path: `` `budgets.py:54` `` or `` `:54` ``.

## House rules
- **Plain language.** Short sentences, active voice, no hype. Written for expert engineers who are new to this codebase.
- **Privacy.** No personal names, family, emails, home-folder paths, hostnames, ports or real ids. Name people by role.
- **Tiers.** This repo is open. Closed-tier pieces appear only as a named box and their connection to the hive. Their internals live in each closed repo's own `docs/schematics/`.

## Add a diagram
Diagrams are mermaid, in a ```` ```mermaid ```` block, one to three per page. Start from the example in [`LEGEND.md`](LEGEND.md). The checker enforces these rules:
- **Short label lines:** every label line is 26 characters or fewer. Break lines with `<br/>` between whole phrases. No other HTML.
- **No dot lists:** never use ` · ` lists. Use commas or `<br/>`.
- **Small:** at most 14 nodes (and about 18 edges). Split a crowded diagram into two.
- **Quoted labels:** quote every label: nodes `A["Label"]`, edges `-->|"label"|`, subgraphs `subgraph id["Title"]` ... `end`. Keep edge labels to 1–3 words.
- **Built versus intended:** built edges are `-->`; intended edges are `-.->` and intended nodes get `:::intended`. Any diagram that uses either declares `classDef intended stroke-dasharray: 5 5;`.
- **Simple syntax:** `flowchart LR` or `flowchart TB`, unique node ids, and no edges to subgraph boundaries.

## Check your work locally
You need Python 3.9 or later (CI uses 3.12) and, to render, Node 22.

Clone the repos side by side, then run from this repo:

```sh
# links, anchors and the mermaid house rules (errors fail)
python3 tools/check_docs.py

# also check `path:line` code refs (warnings) and cross-repo links (errors)
python3 tools/check_docs.py --omegahive ../omegahive --root ..

# render every diagram, as CI does
python3 tools/check_docs.py --quiet --extract-mermaid /tmp/mmd
for f in /tmp/mmd/*.mmd; do
  npx -y @mermaid-js/mermaid-cli@11.4.2 -q -i "$f" -o "${f%.mmd}.svg" || echo "FAILED: $f"
done
```

`--root` looks for each sibling as `<root>/<repo>` or `<root>/apps/<repo>`. `--strict` turns warnings into errors. `/tmp/mmd/index.tsv` maps each `.mmd` file back to its page and line. Open one rendered SVG and look at it.

The [`docs` workflow](.github/workflows/docs.yml) runs the checker and renders every diagram on each push and pull request. CI has no sibling checkouts, so there it only lists cross-repo links and skips code refs. Run the full check locally before you ask for review.

## Review
Every change needs two independent reviewers, neither of them the author. A review is void if the change is altered after it.
