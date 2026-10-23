# Goals and motivations
> Seam-register card. Code refs are to `omegahive` @ 34b0fb3 unless another repo is named. Back to the [register](README.md).

## What it does
Goals (shown as tasks) are units of swarm work with leases, heartbeats, stalls, results and reviews. Motivations are the "why" above tasks and link to them. Wakeups wake a mind on a schedule. Result schemas check a result's shape before a goal is done.

Upstream: [motivation and emotion](https://github.com/PhysixSNET/omegahive-start-here/blob/main/ACKNOWLEDGEMENTS.md#motivation-and-emotion), [attention (ECAN)](https://github.com/PhysixSNET/omegahive-start-here/blob/main/ACKNOWLEDGEMENTS.md#attention-ecan).

## Where it lives
- `hive/core/goals.py:53` `Goals`: `create` `:306`, `claim` `:452`, `heartbeat` `:476`, `result` `:497`, `review` `:209`, lease expiry `expire` `:607`.
- `hive/core/motivations.py:96` `Motivations`; routes installed by `install_routes` `:809`; `tasks` view `:604`; `link` `:674`.
- `hive/core/result_schema.py:1`, `hive/core/schedule.py:91` `Scheduler`.
- Routes: person side `hive/core/app.py:2492-2545`; mind side `:2717-2754`; wakeups `:2568-2585`.

## Contract at its edge
- **Mind routes:** `GET/POST /api/agent/goals`, `POST /api/agent/goals/{id}/claim`, `/heartbeat`, `/result`, `/cancel-ack`. MCP: `hive_goals`, `hive_goal_claim`, `hive_goal_heartbeat`, `hive_goal_result` (`hive/core/mcp.py:93-107`).
- **Person routes:** `GET/POST /api/swarms/{id}/goals`, `PATCH /api/goals/{id}`, `POST /api/goals/{id}/review`; motivations under `/api/motivations` and `/api/tasks`.
- **Shapes:** a result may carry `data`, checked against the goal's `result_schema` (`result_schema.py:1-5`).

## Status and known issues
**Built.** Use motivations and tasks, not the retired Goals or Boards views (`hive/core/boards.py:1` is read-only legacy).

## Tests that guard it
`hive/tests/test_goal_review.py`, `test_result_schema.py`, `test_review_gate.py`, `test_motivations.py`, `test_motivations_correction1.py`, `test_motivation_links.py`, `test_drift_guards.py` (goal leases), `test_phase2_api.py`.

## Swap point
**Yes**, as a work queue. A replacement must keep claim, lease, heartbeat and result semantics, the MCP tool shapes, and swarm scoping. Conformance test: none yet, write one first; `test_drift_guards.py` covers leases.

## Equivalent in the SingularityNET stack
Option to evaluate: goals as atoms in a mind's or swarm's AtomSpace (the V2 body direction), with attention allocation (ECAN) choosing which to pursue.

## Keep criteria
Keep if lease expiry and re-claim are race-free under concurrent minds, and motivation links stay visible only to readers.

## Read next
[01-system/04-request-lifecycle](../01-system/04-request-lifecycle.md), [06-apps/01-programs-contract](../06-apps/01-programs-contract.md), [10-testing/01-test-map](../10-testing/01-test-map.md#components-and-their-tests), [10-testing/04-e2e-scenarios](../10-testing/04-e2e-scenarios.md).
