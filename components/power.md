# Power (Off, Wake all, Stop all)
> Seam-register card. Code refs are to `omegahive` @ 34b0fb3 unless another repo is named. Back to the [register](README.md).

## What it does
Off records which minds were meant to be awake, then stops every mind. Wake all restores exactly those that still can. Stop all records the same snapshot. One snapshot is pending at a time.

## Where it lives
- `hive/core/power.py:1-4`, `:25` `Power` (`hold` `:39`, `record` `:55`, `set` `:82`).
- Routes: `POST /api/hive/stop-all`, `GET|POST /api/hive/power` (`hive/core/app.py:2311-2320`).

## Contract at its edge
`POST /api/hive/power` with the state and an `operation_id`; the snapshot is durable.

## Status and known issues
**Built.** `STATUS.md:31`.

## Tests that guard it
`hive/tests/test_power_modes.py`, `test_stop_reconcile_race.py`.

## Swap point
**No.** Conformance test: none yet.

## Equivalent in the SingularityNET stack
None.

## Keep criteria
Keep if Wake all after a crash restores the same set.

## Read next
[03-minds/02-supervisor-drivers-sandbox](../03-minds/02-supervisor-drivers-sandbox.md), 09-security-and-launch/02-launch-readiness-checklist, incident response (in the private omegahive-security repo; ask Kabir), [08-reviewers/02-invariants, I-M](../08-reviewers/02-invariants.md#i-m-minds-and-the-supervisor).
