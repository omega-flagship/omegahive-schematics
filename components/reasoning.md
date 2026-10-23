# Reasoning libraries (NAL, PLN, NARS)
> Seam-register card. Code refs are to `omegahive` @ 34b0fb3 unless another repo is named. Back to the [register](README.md).

## What it does
Truth functions and inference steps for Non-Axiomatic Logic (NAL), Probabilistic Logic Networks (PLN) and a NARS engine, loaded into every native mind. The LLM calls them as skills. The loop does not call them on its own in this build. The browser runs the same NAL, PLN and lib_hive in MeTTaScript for the personal mind.

Upstream: [NAL, NARS and ONA](https://github.com/PhysixSNET/omegahive-start-here/blob/main/ACKNOWLEDGEMENTS.md#nal-nars-and-ona), [PLN](https://github.com/PhysixSNET/omegahive-start-here/blob/main/ACKNOWLEDGEMENTS.md#pln), [MeTTa and Hyperon](https://github.com/PhysixSNET/omegahive-start-here/blob/main/ACKNOWLEDGEMENTS.md#metta-and-hyperon).

## Where it lives
- `lib_nal.metta` (202 lines; for example `Truth_Deduction` `:8`, `Truth_Revision` `:92`).
- `lib_pln.metta` (309 lines).
- `lib_nars` comes from the PeTTa library, not this repo (`lib_omegaclaw_core.metta:14`).
- Imports: `lib_omegaclaw_core.metta:12-14`. Skills `nars-query`, `nars-derive`, `nal-step`, `pln-step`: `src/skills_reasoning_spaces.metta:1-16`.
- Browser copy: `hive/ui/src/lib/mindSpace/core.ts:1-6`.
- Audit: `docs/reasoning-deviations.md`; references `docs/reference-lib-nal.md`, `reference-lib-pln.md`, `reference-lib-ona.md`.

## Contract at its edge
- **Skills (strings in, strings out):** `(nal-step premise1 premise2)`, `(pln-step premise1 premise2)`, `(nars-query kb term)`, `(nars-derive tasks beliefs)`.
- **Truth value:** `(stv f c)`, the same shape as the commons.
- **Rule:** any change to truth semantics goes to the domain author before merge (`docs/reasoning-deviations.md:7-9`).

## Status and known issues
**Partial.** Callable in every mind (`STATUS.md:34`). Automatic reasoning from the loop is deliberately not wired; a reviewed reasoning foundation and an OBSERVE organ are held (`STATUS.md:49`). Truth functions match the references except documented deviations; PLN stays as it is by the owner's ruling (`STATUS.md:50`). Not activated or bug-fixed in this build (`STATUS.md:73`).

## Tests that guard it
Runtime: `tests/reasoning_space_smoke.metta`, `tests/nars_assimilation_smoke.metta`, `tests/hive_lib_smoke.metta`, `tests/test_omega_surface.py`; probe `docs/probes/nal_pln_reference_probe.metta`. Hive: `hive/tests/test_inventory.py` (skills registered).

## Swap point
**Yes.** A replacement library must keep the skill names and `(stv f c)` shape, and pass the reference probe or document each deviation. Conformance test: `docs/probes/nal_pln_reference_probe.metta` against the reference numbers in `docs/reasoning-deviations.md`.

## Equivalent in the SingularityNET stack
Options to evaluate: the trueagi-io PLN implementation (the audit says the truth block is identical at a pinned commit, `docs/reasoning-deviations.md:26-27`); ONA as the NARS engine; ECAN for choosing what to reason about once the loop calls reasoning.

## Keep criteria
Keep if the domain authors sign off the deviations list, and the team decides whether to wire automatic reasoning before launch or keep it off.

## Read next
[04-knowledge/03-reasoning](../04-knowledge/03-reasoning.md), [04-knowledge/01-metta-and-atomspace](../04-knowledge/01-metta-and-atomspace.md), [07-upgrade-path/02-swap-seams, reasoning](../07-upgrade-path/02-swap-seams.md#5-the-reasoning-libraries), [08-reviewers/02-invariants, I-R](../08-reviewers/02-invariants.md#i-r-reasoning), [08-reviewers/03-review-checklists, reasoning](../08-reviewers/03-review-checklists.md#6-reasoning-and-metta-libraries).
