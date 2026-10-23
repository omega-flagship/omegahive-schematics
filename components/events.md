# Events and live updates
> Seam-register card. Code refs are to `omegahive` @ 34b0fb3 unless another repo is named. Back to the [register](README.md).

## What it does
Pushes live changes to browsers. Any part of the hive publishes a typed event; the event bus fans it out to every connected UI socket, safe from any thread. Before sending, each event is filtered by visibility, so each person sees only what they may.

## Where it lives
- `hive/core/events.py:11` `EventBus`: `bind` `:16`, `subscribe` `:19`, `unsubscribe` `:24`, `publish` `:36-48`.
- Socket `GET /api/events` (WebSocket): `hive/core/app.py:1941-1960`; visibility filter at `:1957`.
- Rules: `EVENT_RULES` `hive/core/visibility.py:232`, `event_visible` `:499`.
- Bound to the running loop at start-up: `hive/core/app.py:155-159`.
- Browser client: `hive/ui/src/api/live.ts:896`.

## Contract at its edge
- **Frame:** JSON `{type: <kind>, at: <time>, ...payload}` (`events.py:37`).
- **Auth:** `?token=<session token>` on the socket; a bad token closes with 4401 (`app.py:1943-1947`).
- **Rule for owners:** every new event kind needs an `EVENT_RULES` entry; publish after commit (`Database.after_commit`, `hive/core/db.py:205`).
- **Mind messages** are separate: they go through the [agent hub](agent-hub.md), not this bus.
- **No new event kind for idle minds.** Health's idle question travels as an ordinary `message`; a personal mind's frames reach its person and not the operator or other admins, and peer `agent:*` messages to it are the person's (the omegahive pull request `port/idle-minds`; see the [visibility page](../05-governance/03-visibility-and-privacy.md#how-it-works)). The UI re-reads the idle routes.

## Status and known issues
**Built.** In-process only: events do not survive a restart, and there is no cross-process bus.

## Tests that guard it
`hive/tests/test_events_websocket.py` (leave, queue release, ping, filtering), `test_visibility.py` (`test_every_published_event_kind_has_a_rule`).

## Swap point
**Yes**, the bus. A replacement (for example a message broker for several hive processes) must keep the frame shape and apply `event_visible` per viewer before delivery. Conformance test: `test_events_websocket.py` plus the event-rule test.

## Equivalent in the SingularityNET stack
No direct equivalent known to this author.

## Keep criteria
Keep if launch runs one hive process per data folder, and a slow browser cannot hold memory (queue release test).

## Read next
[01-system/04-request-lifecycle](../01-system/04-request-lifecycle.md), [05-governance/03-visibility-and-privacy](../05-governance/03-visibility-and-privacy.md), [08-reviewers/02-invariants, I-V](../08-reviewers/02-invariants.md#i-v-visibility-and-privacy), 09-security-and-launch/01-threat-model, TB1 (in the private omegahive-security repo; ask Kabir), [10-testing/01-test-map](../10-testing/01-test-map.md#components-and-their-tests).
