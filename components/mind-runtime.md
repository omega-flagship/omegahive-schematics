# Mind runtime (OmegaClaw)
> Seam-register card. Code refs are to `omegahive` @ 34b0fb3 unless another repo is named. Back to the [register](README.md).

## What it does
The program each native mind runs: OmegaClaw on PeTTa (a MeTTa implementation). It loads a core substrate (skills, memory, reasoning libraries), then modules (channels, senses, the hive client), then attention, then the loop. The loop reads messages, asks the LLM for skill lines, checks each skill with the hive's policy, and runs it.

Upstream: [OmegaClaw Core](https://github.com/PhysixSNET/omegahive-start-here/blob/main/ACKNOWLEDGEMENTS.md#omegaclaw-core), [PeTTa and SWI-Prolog](https://github.com/PhysixSNET/omegahive-start-here/blob/main/ACKNOWLEDGEMENTS.md#petta-and-swi-prolog), [attention (ECAN)](https://github.com/PhysixSNET/omegahive-start-here/blob/main/ACKNOWLEDGEMENTS.md#attention-ecan), [LLM organ](https://github.com/PhysixSNET/omegahive-start-here/blob/main/ACKNOWLEDGEMENTS.md#llm-organ).

## Where it lives
- Entry: `run.metta:1-5`; composition order `lib_omegaclaw.metta:1-11` (substrate, modules, attention, loop).
- Substrate: `lib_omegaclaw_core.metta:7-46` (libraries, skill catalogues, memory, runtime spaces).
- Loop: `src/loop.metta` (hive channel branch at `:74,115`; `initChannels` at `:145`).
- Modules: `modules/loader.metta:1-20`, one folder per module under `modules/` with a `module.toml`.
- Attention: `lib_omegaclaw_attention.metta`, `src/attention_ledger.py`, `src/attention_spin.metta`.
- Started by the supervisor: `hive/supervisor/workspace.py:109-114`; module contract `docs/reference-omegaclaw-module-contract.md`.

## Contract at its edge
- **Toward the hive:** the [agent hub](agent-hub.md) frames and `/api/agent/*` routes, model calls on `/llm/v1` ([gateway](llm-gateway-and-providers.md)), and `POST /api/agent/authorize` before each skill outside the local skip list ([policy](policy-and-approvals.md); the bypasses and K10, K30 are listed there).
- **Toward modules:** `module.toml` (`id`, `kind`, `entrypoint`, `provides`, `requires`, `[env.*]`, `[trace]`), for example `modules/channel_hive/module.toml`.
- **Load-order rule:** PeTTa compiles calls at import time, so modules must load before the loop (`lib_omegaclaw.metta:3-6`).
- **A chosen wait:** a reply that is only `wait` ends the mind's remaining turns, so it makes no model call until new input or its wake; `wait 900` asks for 900 seconds; the runtime's provider-error wait retries after 60 seconds (`src/loop.metta:134-147`, `src/helper.py:264-297`, in the omegahive pull request `port/idle-minds`). See [mind runtime](../03-minds/01-mind-runtime.md#how-it-works).

## Status and known issues
**Built.** `STATUS.md:30`. The runtime is copied into this repo, not linked (`docs/MODULARITY.md:12`). `run.metta:2` fetches the core with `git-import!` at start. Many outer modules are not yet checked against this hive (`STATUS.md:76`). Automatic reasoning from the loop is deliberately not wired (`STATUS.md:49`). Live since the handover snapshot, and brought here by the `port/idle-minds` pull request: a chosen wait makes no model calls (before, the `wait` skill was a no-op and a mind could spend up to 12 calls on one message, all waits).

## Tests that guard it
Runtime suite in `tests/` (`python -m unittest discover -q -s tests`): `test_module_contract.py`, `test_module_organs.py`, `test_skill_surface_contract.py`, `test_syntax_*_smoke.py`, `run_metta_smokes.py`. Hive side: `hive/tests/test_acceptance.py`, `test_phase2_acceptance.py`, `test_inventory.py`. Chosen wait: `tests/test_wait_quiet_runtime.py` and `tests/wait_quiet_runtime_smoke.metta` (with the `port/idle-minds` pull request).

## Swap point
**Yes**, the whole runtime. Any process that speaks the hub frames, the `/api/agent/*` routes and the gateway, and calls `authorize` before every effect, can be a member. External members can join over [MCP](mcp-interface.md) with no runtime at all. Conformance test for a mind: none yet, write one first. Module conformance: `tests/test_module_contract.py`.

## Equivalent in the SingularityNET stack
Options to evaluate: PeTTa (used today) versus the Hyperon Experimental runtime or other MeTTa implementations for the same `.metta` sources; the separate Omega V2 body (closed tier, `omegav2`), whose MeTTa-native organs each need an adapter here.

## Keep criteria
Keep if the runtime suite and the acceptance tests pass from a clean clone with the pinned PeTTa, and the `git-import!` at start is replaced by a pinned, offline source for launch.

## Read next
[03-minds/01-mind-runtime](../03-minds/01-mind-runtime.md), [03-minds/03-modules](../03-minds/03-modules.md), [04-knowledge/01-metta-and-atomspace](../04-knowledge/01-metta-and-atomspace.md), [03-minds/05-models-and-gateway](../03-minds/05-models-and-gateway.md), [07-upgrade-path/02-swap-seams, mind runtime](../07-upgrade-path/02-swap-seams.md#1-the-mind-runtime), [08-reviewers/02-invariants, I-M](../08-reviewers/02-invariants.md#i-m-minds-and-the-supervisor), [10-testing/01-test-map](../10-testing/01-test-map.md#components-and-their-tests).
