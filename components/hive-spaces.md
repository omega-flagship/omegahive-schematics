# Hive spaces and commons (PeTTa, lib_hive)
> Seam-register card. Code refs are to `omegahive` @ 34b0fb3 unless another repo is named. Back to the [register](README.md).

## What it does
Each swarm has a shared MeTTa space of beliefs (its commons) and a shared vocabulary, held in one PeTTa interpreter embedded in the hive. Beliefs carry truth values and evidence stamps. Disjoint evidence is revised; overlapping evidence is resolved by choice, so minds that echo each other cannot inflate confidence. Every change is logged and replayed at start.

Upstream: [MeTTa and Hyperon](https://github.com/PhysixSNET/omegahive-start-here/blob/main/ACKNOWLEDGEMENTS.md#metta-and-hyperon), [PeTTa and SWI-Prolog](https://github.com/PhysixSNET/omegahive-start-here/blob/main/ACKNOWLEDGEMENTS.md#petta-and-swi-prolog), [NAL, NARS and ONA](https://github.com/PhysixSNET/omegahive-start-here/blob/main/ACKNOWLEDGEMENTS.md#nal-nars-and-ona), [MORK and DAS](https://github.com/PhysixSNET/omegahive-start-here/blob/main/ACKNOWLEDGEMENTS.md#mork-and-das).

## Where it lives
- `hive/spaces/service.py:1-8` (contract), `:52-102` `_Interpreter` (one worker thread), `:105` `SpaceService`: `publish` `:214`, `beliefs` `:235`, `belief` `:243`, `query` `:260`; log and replay `:125-139`.
- `hive/spaces/lib_hive.metta`: revision `:22-31`, evidence ids `:49`, access `:63`, vocabulary `:66-88`, integrate `:99`, publish gates `:123-134`, sources `:136`, union view `:148`.
- `hive/spaces/sexpr.py:1-8` (safe parsing at the API edge).
- Host rules: `hive/core/hive.py:1520` `publish` (echo and evidence checks), `:1637` `query`, `:1655` `agent_belief`. Also `hive/core/governance_evidence.py:1` and placement evidence (`hive/core/placement.py:13`).

## Repository maps
With the omegahive pull request `port/repo-map-host`, the same `SpaceService` also holds **read-only repository spaces**. An admin loads a `repo-map/1` map of one repository revision (`POST /api/admin/repo-maps`); the host validates it once, derives inert atoms with one encoder, stores the envelope, nodes, edges and atoms in the database, and mounts the atoms into the space `repo:<repo>@<sha>`, which only the loader writes (`hive/core/repomap.py:316` `RepoMaps`, `load` `:426`, `_mount` `:355`; `hive/spaces/service.py:283-328` `repo_space`, `repo_lock`, `mount_repo`, `unmount_repo`) *(repo-map PR)*. Mounts are serialised per revision under one lock; a failed mount clears the space again, or reports `incomplete` (atoms unknown) when the clear cannot be proven. At start only the newest revision of each repository and pinned ones mount; older ones mount when their header is read. The last 5 revisions per repository are kept, plus pinned ones.

Reads answer from the database rows, not the space: `GET /api/repo-maps`, `/{repo}/presets`, `/{repo}/drift`, `/{repo}/{sha}`, `/{repo}/{sha}/nodes`, `/{repo}/{sha}/nodes/{node_id}`, `POST /{repo}/{sha}/query` with seven presets (`imports`, transitive `potential-dependents`, `defines`, `calls-expression`, `source-search`, `test-doc-links`, `drift`). A hidden map answers 404 like an unknown one; every response fits 256 KiB as sent (or is refused 413 `too_large`, never cut); a read past 2 s answers `partial` with `time_bound`; cursors are HMAC-signed, bound to caller, repository, revision, preset and parameters, and expire after an hour (`hive/core/repomap.py:819-886`) *(repo-map PR)*. Minds read through the `repo-query` skill (`modules/hive/skills.metta:188-190`; `modules/hive/src/hive_commons.py:822`) and MCP members through `hive_repo_query` ([MCP interface](mcp-interface.md)). Tests: `hive/tests/test_repo_map.py` with two synthetic fixtures *(repo-map PR)*.

## Contract at its edge
- **Mind routes:** `POST /api/agent/publish` `{statement, f, c, evidence?, new_evidence?}`, `POST /api/agent/query` `{pattern}`, `GET /api/agent/belief` (`hive/core/app.py:2238-2252`). MCP: `hive_publish`, `hive_query`, `hive_evidence_query`.
- **Truth value:** `(stv f c)`, `0 <= f <= 1`, `0 < c < 1` (`service.py:217-218`).
- **Outcomes:** `adopted`, `revised`, `chosen`, `kept`, `duplicate`, `quarantined`, `denied` (`service.py:24`).
- **Person routes:** `GET /api/swarms/{id}/beliefs`, `/beliefs/detail`, `/vocab` (`app.py:1192-1208`).
- **State:** `spaces.log.jsonl` in the data folder; append-only, not hash-chained.

## Status and known issues
**Built.** `STATUS.md:32-33`. Known issues from the schematics pass:
- **K1:** queries search only the mind's own swarm (`hive/core/hive.py:1642`), though FEATURES CR3 says "and the federation".
- **K2:** `lib_evolve.metta` is a research prototype; `SpaceService` loads only `lib_hive` (`service.py:23`).
- **K3:** quarantine is unreachable through the host: `publish` defaults `open_vocab=True` and adds a member's symbols before the gate (`service.py:214-220`).
- **K4:** quarantined atoms are written to the commons but not logged, so they are lost on restart (`lib_hive.metta:128`; `service.py:225`).
- **K5:** an out-of-range f or c raises `SpaceError` (a `RuntimeError`), but `Hive.publish` catches only `ValueError` (`hive/core/hive.py:1569-1572`). Not yet run.

## Tests that guard it
`hive/tests/test_core_api.py`, `test_drift_guards.py` (echoes), `test_phase2_api.py`, `test_programs_api.py`; runtime `tests/hive_lib_smoke.metta` (lib_hive revision equals lib_nal's).

## Swap point
**Yes**, the space backend. A replacement must keep the routes, the outcome set, disjoint-evidence revision with choice, the vocabulary gate, safe parsing, and durable replay. Conformance test: none yet, write one first; `hive_lib_smoke.metta` is a start.

## Equivalent in the SingularityNET stack
Options to evaluate: embedded PeTTa (today) versus the Hyperon Experimental runtime; MORK as a storage backend (designed, never built, `docs/theory/ledger-provenance-and-das.md:91`); DAS for spaces shared between hives.

## Keep criteria
Keep if K1 to K5 are fixed or ruled, a crash and replay test reproduces the commons byte for byte, and one interpreter thread meets launch load.

## Read next
[04-knowledge/01-metta-and-atomspace](../04-knowledge/01-metta-and-atomspace.md), [04-knowledge/02-beliefs-sharing](../04-knowledge/02-beliefs-sharing.md), [04-knowledge/04-federation](../04-knowledge/04-federation.md), [07-upgrade-path/02-swap-seams, spaces backend](../07-upgrade-path/02-swap-seams.md#3-the-spaces-backend-native-then-mork-then-das), 07-upgrade-path/03-hardening-for-launch (in the private omegahive-security repo; ask Kabir), [08-reviewers/02-invariants, I-K](../08-reviewers/02-invariants.md#i-k-knowledge-and-spaces), [08-reviewers/03-review-checklists, spaces](../08-reviewers/03-review-checklists.md#5-spaces-and-the-commons), [10-testing/04-e2e-scenarios, scenario 5](../10-testing/04-e2e-scenarios.md#5-shared-beliefs-survive-a-crash-and-a-restore).
