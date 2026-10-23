# Flows
> Seam-register card. Code refs are to `omegahive` @ 34b0fb3 unless another repo is named. Back to the [register](README.md).

## What it does
OmegaFlow: work described as a typed flow graph with immutable revisions. A person adopts a revision and starts a run; the hive turns it into goals and reconciles the run as goals finish. Minds can draft flows and register flow skills.

## Where it lives
- `hive/core/flows.py:1-4` (contract), `:35` `Flows`: `publish` `:267`, `plan` `:300`, `adopt` `:334`, `start` `:350`, `reconcile` `:496`; mind side `register_skill` `:150`, `agent_start` `:193`.
- IR: `hive/flow_ir/` (`model.py`, `symbolic.py`, `admission.py`); editor `hive/flow_studio/`; written contract `hive/FLOWS.md`.
- Routes: `hive/core/app.py:2365-2486` (person and mind sides).

## Contract at its edge
- **IR:** `omegaflow/1` (`hive/FLOWS.md:5-7`).
- **Routes:** `POST /api/flows/validate`, `POST /api/swarms/{id}/flows`, `POST /api/flows/{id}/revisions/{n}/adopt`, `/runs`; minds `/api/agent/flows*`, `/api/agent/flow-runs/{rid}`.
- **Policy:** `hive-flow-publish` needs an exact allow rule (`hive/core/policy.py:21`).

## Status and known issues
**Built** (named a "candidate" in its own header).

## Tests that guard it
`hive/tests/test_flows.py`.

## Swap point
**Yes.** A replacement must produce ordinary goals in the swarm and reconcile on goal completion. Conformance test: none yet, write one first.

## Equivalent in the SingularityNET stack
Option to evaluate: flows as MeTTa programs or atoms that a mind can reason over, since the IR already has a symbolic form (`hive/flow_ir/symbolic.py`).

## Keep criteria
Keep if a run survives a hive restart mid-flow and cancellation reaches every child goal.

## Read next
[01-system/02-hive-server-map](../01-system/02-hive-server-map.md), [goals and motivations](goals-and-motivations.md), [10-testing/01-test-map](../10-testing/01-test-map.md#components-and-their-tests), [10-testing/04-e2e-scenarios](../10-testing/04-e2e-scenarios.md).
