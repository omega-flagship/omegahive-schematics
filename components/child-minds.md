# Child minds
> Seam-register card. Code refs are to `omegahive` @ 34b0fb3 unless another repo is named. Back to the [register](README.md).

## What it does
A team's controller mind runs child minds for one person's request, under leases, with a prompt the child must acknowledge. Live spawning is off unless the operator turns it on.

## Where it lives
- `hive/core/minds.py:1-25` (contract), `:157` `Minds`; spawn gate `:578`; signed child tokens `:1056-1063`.
- Routes: `hive/core/app.py:3159-3212` (`/api/agent/minds*`, `/api/requests`, `/api/teams/{id}/children*`); acknowledgement frame `prompt_ack` on the hub (`app.py:2045-2050`).

## Contract at its edge
- **Setting:** `HIVE_MIND_SPAWN=1` (`minds.py:20`).
- **Routes:** `POST /api/agent/minds`, `/api/agent/minds/{id}/prompt`, `/control`; admins `POST /api/requests`.

## Status and known issues
**Partial.** Built and tested; activation held; never spawned live (`STATUS.md:53`).

## Tests that guard it
`hive/tests/test_mind_fitness_*.py`, `test_bounded_run.py`, `test_mind_control.py`.

## Swap point
**No** for now. Conformance test: none yet.

## Equivalent in the SingularityNET stack
Option to evaluate: the society layer of the Omega V2 design (closed tier) for how many minds cooperate.

## Keep criteria
Decide before launch whether it stays off. Turning it on needs a live run with the sandbox on.

## Read next
[03-minds/01-mind-runtime](../03-minds/01-mind-runtime.md), [capability tokens and delegation](capability-tokens-and-delegation.md), [03-minds/02-supervisor-drivers-sandbox](../03-minds/02-supervisor-drivers-sandbox.md), 09-security-and-launch/01-threat-model, TB4 (in the private omegahive-security repo; ask Kabir), [08-reviewers/02-invariants, I-M](../08-reviewers/02-invariants.md#i-m-minds-and-the-supervisor).
