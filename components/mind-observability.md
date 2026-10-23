# Mind observability (traces, health, idle monitor, inventory)
> Seam-register card. Code refs are to `omegahive` @ 34b0fb3 unless another repo is named. Back to the [register](README.md).

## What it does
Shows what each mind did and can do. Minds post traces of their commands; health classifies errors across minds from existing records; the inventory lists the skills a mind actually registered, from a boot receipt it posts after loading. Old traces are archived, never deleted.

**Health and idle monitor.** Health also watches for idle minds. A pass in the reconcile loop, at most once a minute, notices an awake mind that has (a) owed work: a goal it holds with no heartbeat for an hour, an open goal assigned to it, or a message from a person or mind with no reply for an hour (team rooms, the Coffee Room, Ask turns and hive notes are not counted); (b) model spend with no input for an hour; or (c) no input and no output for an hour (the "silent" signal, for a mind that now answers only `wait` and so barely spends). It asks that mind ONE question through the normal message path, never twice in one idle stretch and on its own at most every 6 hours, and records the question and the mind's next message in that conversation. It never sleeps or limits a mind; a person decides, with Remind or the existing Sleep. A personal mind's question goes to its person's own chat ([visibility page](../05-governance/03-visibility-and-privacy.md#how-it-works)). All of this is live since the handover snapshot and arrives here with the omegahive pull request `port/idle-minds`; the refs below marked *(idle-minds PR)* point at that branch.
## Where it lives
- `hive/core/health.py:1-4`, `:75` `Health`; `hive/core/inventory.py:1-4`, `:80` `Inventory` (`record` `:179`, `view` `:283`); `hive/core/archive.py:34`.
- Routes: traces `hive/core/app.py:2549-2560`, `POST /api/agent/trace` `:2692`, health `:2613-2638`, inventory `:2645-2674`, logs `:1921`.
- Idle monitor *(idle-minds PR)*: `hive/core/health.py:290` `IdleWatch` (`owed` `:312`, `facts` `:346`, `question` `:368`, `ask` `:428`, `run` `:454`, `remind` `:485`, `view` `:495`); the pass in the reconcile loop `hive/core/app.py:194`; routes `:2650-2696`; table `health_idle` and column `agents.last_input_at` (`hive/core/db.py:85-92`, `:148`).

## Contract at its edge
`POST /api/agent/inventory` (boot receipt, with a nonce from `GET /api/agent/inventory/nonce`); MCP `hive_capabilities` returns the same view.

Idle monitor *(idle-minds PR)*: `GET /api/health/idle` (every awake mind and every mind asked in the last 7 days, worst first, with the `window` values), `GET /api/agents/{id}/health/idle` (one mind with its last 20 records) and `POST /api/agents/{id}/health/remind` (ask now; 409 `not_awake`; two Reminds within 60 s are one question). Readers are an admin or the mind's owner (its creator, or the person whose personal mind it is); anyone else gets 404. Another person's personal mind is hidden unless the admin audits with `?include=all` or `?include=personal`, whatever its visibility; a Remind on a personal mind is its person's alone (403 `personal_mind` for an auditing admin). Every row carries the per-viewer flags `is_mine`, `may_remind` and `may_sleep` *(idle-minds r2.5 PR)*. The question arrives with sender `hive:health` and `extra = {event: health_question, question_id}`. No new live event kind.

## Status and known issues
**Built.** The MCP `hive_capabilities` description is stale (see [MCP interface](mcp-interface.md)). Idle monitor: built and live since the handover snapshot, arriving here with the `port/idle-minds` pull request. K65 (a public or shared personal mind's idle record readable without explicit audit) is fixed by `port/idle-minds-r2.5`. Health's **Idle minds** section in the UI shows the record, its history and Remind and Sleep, offered only by the host's flags and for an awake mind, and bound to the identity the act started under (`hive/ui/src/features/health/IdleMinds.tsx:39`, `hive/ui/src/api/idleMinds.ts:282`) *(health-idle UI PR)*. The idle pass runs inside the reconcile loop's one `try`, so K20 applies to it too.

## Tests that guard it
`hive/tests/test_health.py`, `test_inventory.py`, `test_archive.py`, `test_trace_truncation.py`; idle monitor `hive/tests/test_idle_minds.py` *(idle-minds PR)*.

## Swap point
**Yes**, as an export: traces could feed an outside observability stack. Conformance test: none yet.

## Equivalent in the SingularityNET stack
No direct equivalent known to this author.

## Keep criteria
Keep if traces never carry personal-turn content, archives are readable after rotation, and the idle monitor stays a question, never a limit, with a personal mind's record readable only by its person or an explicit audit.

## Read next
[03-minds/01-mind-runtime](../03-minds/01-mind-runtime.md), [01-system/03-state-and-storage](../01-system/03-state-and-storage.md), 09-security-and-launch/02-launch-readiness-checklist, observability (in the private omegahive-security repo; ask Kabir), [10-testing/03-gaps](../10-testing/03-gaps.md).
