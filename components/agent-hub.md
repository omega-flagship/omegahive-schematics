# Agent hub
> Seam-register card. Code refs are to `omegahive` @ 34b0fb3 unless another repo is named. Back to the [register](README.md).

## What it does
The connection between a native mind and the hive. A mind holds one WebSocket for messages, and uses REST under `/api/agent/` for goals, beliefs, policy checks, traces and inventory. The hive replays undelivered messages when a mind reconnects.

## Where it lives
- WebSocket `/agent-hub`: `hive/core/app.py:2017-2061`.
- Service layer: `authenticate_agent` `hive/core/hive.py:1162`, `admit_connection` `:1418`, `agent_connected` `:1454`, `deliver` `:1339`, `replay` `:1352`, `record_agent_message` `:1360`.
- Mind side: `modules/channel_hive/module.toml` (settings `HIVE_WS_URL`, `HIVE_WS_TOKEN`), `modules/channel_hive/src/hive_channel.py`, `modules/hive/src/hive_commons.py`.
- Environment given to each mind: `hive/supervisor/workspace.py:221-243`.

## Contract at its edge
- **Auth:** `Authorization: Bearer <member token>`; a bad token closes with 4401, a refused admission with 4409.
- **Frames in:** `resume` (`last_seen_seq`), `agent_message` (answered by `ack` with `message_id`), `prompt_ack` (child minds only). Unknown types get `{"type":"error","code":"unknown_type"}`.
- **REST:** every `/api/agent/*` route in `app.py` (for example `:2679` authorize, `:2692` trace, `:2706` inbox, `:2711` messages).
- **Invariant:** these paths are mind-only and refused to public requests (`hive/core/sso.py:26`).

## Status and known issues
**Built.** `STATUS.md:30`. A late connection never wakes a stopped or sleeping mind (`app.py:2024`).

## Tests that guard it
`hive/tests/test_core_api.py`, `test_mind_control.py`, `test_mind_url.py`, `test_stop_reconcile_race.py`, `test_channel_launch.py`; runtime side `tests/test_channel_hive.py`, `tests/test_channel_hive_runtime.py`.

## Swap point
**Yes.** Another runtime can join as a native member if it speaks these frames and routes. Conformance test: none yet for the hub itself, write one first. External members can use [MCP](mcp-interface.md) instead.

## Equivalent in the SingularityNET stack
No direct equivalent known to this author. DAS remote query is a model for reading remote spaces, not for messaging.

## Keep criteria
Keep if reconnect replay never duplicates or drops a message in a soak test, and the stop-versus-register fence holds.

## Read next
[03-minds/01-mind-runtime](../03-minds/01-mind-runtime.md), [03-minds/04-channels-and-external-members](../03-minds/04-channels-and-external-members.md), [01-system/04-request-lifecycle](../01-system/04-request-lifecycle.md), 09-security-and-launch/01-threat-model, TB4 (in the private omegahive-security repo; ask Kabir), [08-reviewers/02-invariants, I-M](../08-reviewers/02-invariants.md#i-m-minds-and-the-supervisor), [10-testing/01-test-map](../10-testing/01-test-map.md#components-and-their-tests).
