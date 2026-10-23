# Ask and conductor
> Seam-register card. Code refs are to `omegahive` @ 34b0fb3 unless another repo is named. Back to the [register](README.md).

## What it does
The text and voice Ask on every page. The host routes a request to a swarm's coordinator, or to the person's personal mind. One exception: in a swarm with no coordinator, a native mind the request explicitly addressed answers under the same checks (`hive/core/ask.py:293-312`). When the conductor is on, one host model loop answers instead and steers the screen with typed acts (navigate, point, fill, and so on). Handing work to a swarm only records an intent; the person sends it.

## Where it lives
- `hive/core/ask.py:231` `Ask`; routing `orchestrator` `:293`; turn admission `create` `:633`; content-free personal turns `content_free` `:762`.
- `hive/core/conductor.py:71` `enabled()`; limits and billing in the docstring `:18-30`; act checks `check_act` `:337`; `TurnState` `:529`.
- `hive/core/ask_intents.py`, `hive/core/personal.py:52` `PersonalMinds`, `hive/core/personal_inbox.py`.
- Routes: `hive/core/app.py:1554-1763` (`/api/ask*`, `/api/me/ask`), personal mind `:1774-1788`.
- UI: `hive/ui/src/features/ask/` (`AskHost.tsx`, `conductor.ts`, `voice.ts`).

## Contract at its edge
- **Routes:** `POST /api/ask` opens a turn; `GET /api/ask/{op}` pages its frames; `POST /api/ask/{op}/acts/{act}/result` returns an act result; `POST /api/ask/{op}/intents` and `/api/ask/intents/{id}/submit`.
- **Frames:** `ask` events, in order, to the asker only; `answer` frames with `delta`, then one whole `answer`, then `done` (`conductor.py:18-20`).
- **Limits:** 32 acts, 12 model calls, 120 s, and a spend cap through cost reservations (`conductor.py:22-25`).
- **Settings:** `HIVE_ASK_CONDUCTOR`, `HIVE_ASK_CONDUCTOR_MODEL`, `HIVE_ASK_CONDUCTOR_TURN_USD`, `HIVE_ASK_MEMORY`, `HIVE_ASK_TIMEOUT_SECONDS` (`conductor.py:71-95`, `ask.py:120`).

## Status and known issues
**Built**, conductor off by default. `STATUS.md:28-29`. Personal-mind turns require the conductor and keep no content on the host (`ask.py:24-31`). Live since the handover snapshot and brought here by the omegahive pull requests `port/surface-followups-r4` and `port/demo-mode-fix`: the thread line calls a mind the orchestrator only when it is the swarm's coordinator (the follow-up noted in FEATURES PM23), and the Tasks page's filters and open tasks reach the Ask.

## Tests that guard it
`hive/tests/test_ask.py`, `test_ask_conductor.py`, `test_ask_intents.py`, `test_ask_memory.py`, `test_personal_ask_control.py`, `test_personal_mind*.py`; UI tests in `hive/ui/src/features/ask/*.test.ts`.

## Swap point
**Yes**, the conductor. A replacement must speak action vocabulary v1, respect the per-turn limits and reservations, and record (never submit) intents. Conformance test: none yet, write one first; `test_ask_conductor.py` is the starting point.

## Equivalent in the SingularityNET stack
Option to evaluate: a MeTTa-native conductor that runs inside the person's mind (Hyperon or PeTTa), with the LLM as one organ, instead of a host-side model loop.

## Keep criteria
Keep if the turn limits hold under load tests, personal turns stay content-free on read and on audit, and the action vocabulary covers the launch UI.

## Read next
[02-ask-and-ui/01-ask-and-conductor](../02-ask-and-ui/01-ask-and-conductor.md), [01-system/04-request-lifecycle](../01-system/04-request-lifecycle.md), [05-governance/02-budgets-and-spend](../05-governance/02-budgets-and-spend.md), [03-minds/05-models-and-gateway](../03-minds/05-models-and-gateway.md), [08-reviewers/02-invariants, I-Q](../08-reviewers/02-invariants.md#i-q-the-ask), [10-testing/01-test-map](../10-testing/01-test-map.md#components-and-their-tests).
