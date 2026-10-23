# Native Tools
> Seam-register card. Code refs are to `omegahive` @ 34b0fb3 unless another repo is named. Back to the [register](README.md).

## What it does
Reviewed native Tools that a mind can be given, separate from runtime modules and off by default. Each request runs in a disposable child process. A receipt hash binds bytes; it is not a signature or authority.

## Where it lives
- `hive/core/tools.py:1-5`, `:153` `ToolRegistry`; `hive/core/tools_worker.py:1`.
- Catalogue route `GET /api/tools` (`hive/core/app.py:1220-1226`); validation when a mind is created or edited (`hive/core/hive.py:920-930`).
- The Tools app is its own open repo (`omega-tools`).

## Contract at its edge
A mind's `options.tools` names the tools; they need the local driver (`hive/core/hive.py:855-856`).

## Status and known issues
**Built**, default disabled.

## Tests that guard it
`hive/tests/test_tools.py`, `test_tools_api.py`.

## Swap point
**Yes**, per tool family. Conformance test: none yet.

## Equivalent in the SingularityNET stack
Option to evaluate: marketplace AI services as tool families.

## Keep criteria
Keep if each enabled family has a review and runs only in the child process.

## Read next
[06-apps/apps/omega-tools](../06-apps/apps/omega-tools.md), [03-minds/03-modules](../03-minds/03-modules.md), [08-reviewers/03-review-checklists, apps](../08-reviewers/03-review-checklists.md#9-apps-and-the-programs-contract), [10-testing/01-test-map](../10-testing/01-test-map.md#components-and-their-tests).
