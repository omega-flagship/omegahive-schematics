# Between swarms (connections, services, requests)
> Seam-register card. Code refs are to `omegahive` @ 34b0fb3 unless another repo is named. Back to the [register](README.md).

## What it does
How swarms work together inside one hive. A connection agreement says who, why, what is shared, for how long and on what budget. A cross-swarm request links a goal in one swarm to a goal the hive creates in another; it confers no access by itself. Artifacts have immutable revisions, and reviewers raise findings on them.

## Where it lives
- `hive/core/connections.py:1-4`, `:41` `Connections` (`create` `:120`, `allows_request` `:255`, `expire` `:243`).
- `hive/core/collab.py:1-4`, `:201` `Collab` (`create_request` `:472`, `add_revision` `:637`, `raise_finding` `:779`, `complete_review` `:999`, `service_catalogue` `:257`).
- Routes: connections `hive/core/app.py:3226-3258`, swarm services and artifacts `:2973-3026`, requests, artifacts and findings `:3268-3354`.

## Contract at its edge
- **Routes:** `POST /api/connections`, `POST /api/connections/{id}/{action}`; minds `POST /api/agent/requests`, `/api/agent/artifacts`, `/api/agent/findings`; MCP `hive_request`, `hive_revision_read`, `hive_artifact_read`.
- **Rule:** receiving swarms opt in to the request kinds they serve (`collab.py:3-4`).

## Status and known issues
**Built.** Cross-hive requests are not built (see [federation](federation.md)).

## Tests that guard it
`hive/tests/test_connections.py`, `test_connection_services.py`, `test_collab.py`, `test_swarm_artifacts.py`, `test_app_artifacts.py`, `test_request_visibility.py`, `test_planning_review_context.py`.

## Swap point
**No** for now; it is part of the hive's core model. Conformance test: none yet.

## Equivalent in the SingularityNET stack
Option to evaluate: marketplace service descriptions for the catalogue of what a swarm serves.

## Keep criteria
Keep if expiry ends every scope on time and a request never grants claim or source access by itself.

## Read next
[01-system/02-hive-server-map](../01-system/02-hive-server-map.md), [06-apps/01-programs-contract](../06-apps/01-programs-contract.md), [08-reviewers/02-invariants, I-V](../08-reviewers/02-invariants.md#i-v-visibility-and-privacy), [10-testing/01-test-map](../10-testing/01-test-map.md#components-and-their-tests).
