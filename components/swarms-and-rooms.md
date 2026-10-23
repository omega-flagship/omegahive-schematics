# Swarms and rooms
> Seam-register card. Code refs are to `omegahive` @ 34b0fb3 unless another repo is named. Back to the [register](README.md).

## What it does
A swarm is a group of minds and people with its own commons, coordinator and limits. Rooms hold conversations: DMs, groups, channels and projects are one thing. Each swarm has a team room with @mentions. Sessions are focused threads with one mind, built on rooms.

## Where it lives
- Swarms in the service layer: `hive/core/hive.py:662` `create_swarm`, `:211` `update_swarm`, `:314` `swarms`, `:482` `delete_swarm`.
- `hive/core/rooms.py:98` `Rooms`; team rooms `team_room` `:566`, `sync_team` `:586`; mentions `:775`; person posts `:812`; mind posts `:886`.
- `hive/core/sessions.py` (focused sessions), `hive/core/roles.py` (role bundles).
- Routes: swarms `hive/core/app.py:1143-1220`, rooms `:1472-1520`, sessions `:1796-1838`, mind room access `:1842-1846`, roles `:678-698`.

## Contract at its edge
- **Routes:** `GET/POST /api/swarms`, `PATCH/DELETE /api/swarms/{id}` (with `delete-preview`), `GET/POST /api/rooms`, `POST /api/rooms/{id}/messages`, `POST /api/swarms/{id}/team-room/repair`.
- **Mind side:** `GET /api/agent/rooms`, `POST /api/agent/rooms/{id}/messages`.
- **Fields:** a swarm has `name`, `owner`, `visibility`, `shared_with` and a coordinator (`hive.py:662`).
- **Setting:** `HIVE_LOCAL_ONLY_SWARMS` makes a swarm refuse outside model calls (enforced in the gateway, `hive/core/gateway.py:230-240`).

## Status and known issues
**Built.** `STATUS.md:30-31`. Organising the hive into folders and screens and nesting hives without limit is partly built (`STATUS.md:75`).

## Tests that guard it
`hive/tests/test_rooms.py`, `test_team_rooms.py`, `test_sessions.py`, `test_swarm_delete.py`, `test_swarm_archive.py`, `test_roles_api.py`, `test_holarchy_api.py`, `test_coffee_room.py`.

## Swap point
**No.** Swarms are the hive's core grouping, and most other cards key on `swarm_id`. Conformance test: none yet, write one first.

## Equivalent in the SingularityNET stack
No direct equivalent known to this author. Option to evaluate: represent swarm membership and rooms as atoms in a shared space, so that federation (see [federation](federation.md)) can move them with the commons.

## Keep criteria
Keep if delete and archive previews match what is removed, team rooms repair cleanly after member changes, and nested swarms are either finished or switched off for launch.

## Read next
[01-system/01-system-overview](../01-system/01-system-overview.md), [01-system/03-state-and-storage](../01-system/03-state-and-storage.md), [03-minds/04-channels-and-external-members](../03-minds/04-channels-and-external-members.md), [08-reviewers/02-invariants, I-V](../08-reviewers/02-invariants.md#i-v-visibility-and-privacy), [10-testing/01-test-map](../10-testing/01-test-map.md#components-and-their-tests).
