# Lab and Evolve
> Seam-register card. Code refs are to `omegahive` @ 34b0fb3 unless another repo is named. Back to the [register](README.md).

## What it does
The Lab runs test suites and benchmarks from the UI as child processes with their own scratch data, and keeps their history. Evolve keeps immutable, swarm-scoped claims and experiment registrations; the Evolve app itself is a closed-tier plugin, and these modules are its host-side records only.

## Where it lives
- `hive/core/lab.py:1-4`, `:48` `Lab`; routes `hive/core/app.py:2329-2360`; benchmarks `hive/bench/`, `omegabench/`.
- `hive/core/evolve.py:21` `EvolveRegistry`; `evolve_preflight.py`, `evolve_projection.py`, `evolve_seed.py`, `evolve_state.py`; reached by apps through `ProgramContext.evolve_*` (`hive/core/programs.py:200-229`).
- `hive/spaces/lib_evolve.metta` (research prototype; not loaded by the hive, K2).
- Closed tier: `hive/plugins/omegaevolve` (`docs/MODULARITY.md:20`).

## Contract at its edge
Lab: `GET /api/lab/suites`, `POST /api/lab/runs`, `GET /api/lab/scorecard`. Evolve: only through the program context.

## Status and known issues
**Partial.** Built. In the UI, Compare and the Epistemic board judge a measure only when it is comparable (declared units, same definition and direction), and Lab shows OmegaEvolve's recorded contributions read-only in a predictive-coding band, never counted in totals, Compare, History or Health (omegahive pull requests `port/lab-compare` and `port/lab-pc-band`; `hive/ui/src/features/lab/stallCompare.ts`, `hive/ui/src/features/lab/pc/`). **K2:** FEATURES CR9 marks `lib_evolve.metta` live, but `SpaceService` loads only `lib_hive` (`hive/spaces/service.py:23`).

## Tests that guard it
`hive/tests/test_lab_api.py`, `test_evolve*.py`, `test_omegabench_*.py`; UI `features/lab/labCompare.r1.test.ts`, `labCompare.r1_1.test.ts`, `features/lab/pc/pcFamily.test.ts`, `pcFamilyScope.test.ts` (with the pull requests above).

## Swap point
**Yes**, the benchmark runner, if it keeps scratch isolation. Conformance test: none yet.

## Equivalent in the SingularityNET stack
No direct equivalent known to this author.

## Keep criteria
Keep if a Lab run is shown never to touch the live data folder.

## Read next
[06-apps/02-app-lifecycle](../06-apps/02-app-lifecycle.md), [04-knowledge/01-metta-and-atomspace](../04-knowledge/01-metta-and-atomspace.md), [07-upgrade-path/01-intended-evolution](../07-upgrade-path/01-intended-evolution.md), [10-testing/01-test-map](../10-testing/01-test-map.md#components-and-their-tests).
