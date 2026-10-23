# SQLite state
> Seam-register card. Code refs are to `omegahive` @ 34b0fb3 unless another repo is named. Back to the [register](README.md).

## What it does
The hive's control-plane store: people, minds, swarms, rooms, goals, policy, approvals, usage, reservations and the rest. Beliefs are not here; they live in the [hive spaces](hive-spaces.md). One hive process owns one data folder for its whole life, enforced by an exclusive file lock.

## Where it lives
- `hive/core/db.py:1` (purpose), `:95` `Database`; WAL and foreign keys `:100-101`; `transaction` `:171`; `after_commit` `:205`; `erase` with secure delete `:217-230`; `secure_writes` `:236`; `guarded_execute` `:256`.
- Opened as `<data dir>/hive.db` at `hive/core/hive.py:85`. Most feature modules create their own tables in their constructors.
- `hive/core/exclusive.py:1-5` (one process per `HIVE_DATA_DIR`, `hive.lock`, the one startup recovery).
- `hive/core/archive.py:1` (trace archive and log rotation; nothing a mind did is deleted, only moved).
- Other files in the data folder: `spaces.log.jsonl`, mind workspaces, assets.

## Contract at its edge
- **Setting:** `HIVE_DATA_DIR`.
- **API inside the hive:** `execute`, `one`, `all`, `insert`, `update`, `transaction()` context manager, `after_commit(fn)` for events that must follow a commit.
- **Rule:** writes that must not leave readable remnants (personal content) go through `erase` or `secure_writes`.

## Status and known issues
**Built.** Single host by choice. Settings are read across many modules; `config.py` holds only some (`docs/MODULARITY.md:54-57`).

## Tests that guard it
`hive/tests/test_startup_exclusive.py`, `test_guarded_save.py`, `test_archive.py`, `test_trace_truncation.py`, `test_program_publish_atomic.py`, plus every API test (they all run on a real SQLite file).

## Swap point
**No** for launch: SQL is spread across about 75 modules, so a swap means a data-access layer first. Conformance test: none yet, write one first.

## Equivalent in the SingularityNET stack
Option to evaluate: making the AtomSpace the state of record (the V2 body direction, `docs/EARLIER_EXPERIMENTS.md:38`), with DAS behind it for scale. That is a large change, not a drop-in.

## Keep criteria
Keep if the launch load fits one host, backups and restore are tested with WAL, and the exclusive lock is shown to block a second process.

## Read next
[01-system/03-state-and-storage](../01-system/03-state-and-storage.md), [01-system/02-hive-server-map](../01-system/02-hive-server-map.md), [08-reviewers/02-invariants, I-S](../08-reviewers/02-invariants.md#i-s-state-and-storage), 09-security-and-launch/02-launch-readiness-checklist, data and backup (in the private omegahive-security repo; ask Kabir), [10-testing/04-e2e-scenarios, scenario 5](../10-testing/04-e2e-scenarios.md#5-shared-beliefs-survive-a-crash-and-a-restore).
