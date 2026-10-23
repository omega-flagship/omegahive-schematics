# Supervisor and drivers
> Seam-register card. Code refs are to `omegahive` @ 34b0fb3 unless another repo is named. Back to the [register](README.md).

## What it does
Starts, stops and restarts mind processes and keeps each in its desired state. It runs inside the hive process. It prepares each mind's workspace (prompt, tools, token, environment) and hands it to a driver: a local process (the default) or a Docker container.

Upstream: [PeTTa and SWI-Prolog](https://github.com/PhysixSNET/omegahive-start-here/blob/main/ACKNOWLEDGEMENTS.md#petta-and-swi-prolog), [OmegaClaw Core](https://github.com/PhysixSNET/omegahive-start-here/blob/main/ACKNOWLEDGEMENTS.md#omegaclaw-core).

## Where it lives
- `hive/supervisor/drivers.py:353` `Supervisor` (drivers built at `:357-362`); built in `create_app` at `hive/core/app.py:113`.
- Driver interface `hive/supervisor/drivers.py:62-80` `Driver` (`start`, `stop`, `status`, `logs`, `execution`).
- `LocalDriver` `:94` (sandbox switch `:184-187`); `DockerDriver` `:243` (image and network settings `:254-255`); Iter preflight `:36`.
- `hive/supervisor/workspace.py:65` `Workspace`: `command` `:109`, `create` `:167`, `env` `:221`.
- Restore and adoption after restart: see `hive/tests/test_local_driver_adopt.py`.

## Contract at its edge
- **Driver interface:** `start(agent, env)`, `stop(agent_id)`, `status(agent_id)`, `logs(agent_id, tail)`, `execution(agent_id)`.
- **Mind command:** `sh <PeTTa>/run.sh <workspace>/run.metta --silent`, or `python3 iter.py` for Iter minds (`workspace.py:109-114`).
- **Mind environment:** `HIVE_WS_URL`, `HIVE_WS_TOKEN`, `HIVE_API_URL`, `HIVE_AGENT_ID`, `HIVE_LLM_URL`, `HIVE_LLM_TOKEN` (`workspace.py:234-243`).
- **Settings:** a mind's `driver` field, `HIVE_AGENT_IMAGE`, `HIVE_DOCKER_NETWORK`, `HIVE_ITER_IMAGE`, `HIVE_ALLOW_LOCAL_ITER`, `HIVE_MIND_SANDBOX`.

## Status and known issues
**Partial.** Local driver live; Docker driver unverified and refused on the cloud (`docs/FEATURES.md:108-109`). Docker uses host networking by default, without hardening flags (`STATUS.md:55`).

## Tests that guard it
`hive/tests/test_docker_driver.py`, `test_docker_driver_stop.py`, `test_local_driver_adopt.py`, `test_agent_driver.py`, `test_stop_reconcile_race.py`, `test_mind_control.py`, `test_mind_url.py`.

## Swap point
**Yes.** A new driver (for example Kubernetes or a VM) implements the `Driver` interface and must report a stop only when the process is observed stopped. Conformance test: none yet, write one first.

## Equivalent in the SingularityNET stack
No direct equivalent known to this author. Option to evaluate: a hosting layer the SingularityNET team already runs for agents, behind the same `Driver` interface.

## Keep criteria
Keep the local driver if restart adoption never makes a duplicate or orphan. Keep the Docker driver only after it gets hardening flags and a live verification.

## Read next
[03-minds/02-supervisor-drivers-sandbox](../03-minds/02-supervisor-drivers-sandbox.md), [05-governance/04-isolation](../05-governance/04-isolation.md), [07-upgrade-path/02-swap-seams, drivers](../07-upgrade-path/02-swap-seams.md#9-the-sandbox-and-drivers), 07-upgrade-path/03-hardening-for-launch (in the private omegahive-security repo; ask Kabir), 09-security-and-launch/01-threat-model, TB4 (in the private omegahive-security repo; ask Kabir), [08-reviewers/03-review-checklists, minds](../08-reviewers/03-review-checklists.md#7-minds-supervisor-drivers-and-sandbox).
