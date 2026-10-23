# Budgets
> Seam-register card. Code refs are to `omegahive` @ 34b0fb3 unless another repo is named. Back to the [register](README.md).

## What it does
Spending limits at every level: hive, swarm, mind, key and person. Every paid call is checked against every rule that applies, at its worst-case cost, before it is made. A durable reservation holds that cost until the call settles. Automatic limits are derived from one hive total.

## Where it lives
- `hive/core/budgets.py:1-17` (rule shape), `:43` `Budgets`: `set` `:54`, `applicable` `:263`, `check` `:294`, `member_allowance` `:103`, `hard_cap` `:140`.
- `hive/core/cost_reservations.py:22` `Reservations`: `reserve` `:119`, `dispatch` `:155`, `settle` `:170`; startup recovery `:40`; `expire_unknown` `:332`.
- `hive/core/limits_auto.py:1`, `hive/core/limits_view.py:1` (the Limits page read model).
- Routes: `hive/core/app.py:1038-1069` (rules), `:2205-2217` (reservations and overruns), `:1928-1933` (usage).

## Contract at its edge
- **Rule:** `(scope, period, limit_usd)`; scope `hive`, `swarm:<id>`, `agent:<id>`, `person:<id>`, `key:<id>` or `every-mind`; period `day`, `month` or `total` (`budgets.py:3-5`).
- **Refusal:** 402 `spend_limit` from the first rule a call would break (`budgets.py:7-8`).
- **Settings:** `HIVE_BUDGET_USD`, `HIVE_SWARM_MONTHLY_USD`, `HIVE_MEMBER_MONTHLY_USD`, `HIVE_PERSON_REQUEST_CEILING_USD`, `HIVE_ASK_CONDUCTOR_TURN_USD` (`budgets.py:149-172`).
- **Reservation states:** reserved, dispatched, unknown, settled; unknown holds expire after 24 h at their held worst case (`app.py:202-211`, `cost_reservations.py:329`).

## Status and known issues
**Built.** `STATUS.md:37`. Spend is not activity: recording a paid call moves only `spent_usd`, never `last_active_at` or the idle signal `last_input_at`, so a mind spending with nothing coming in still idle-sleeps on its `idle_sleep_minutes` and is noticed by Health (`hive/core/hive.py:1811-1823` in the omegahive pull request `port/idle-minds`; live since the handover snapshot). Before, every paid call counted as activity. See [mind observability](mind-observability.md).

## Tests that guard it
`hive/tests/test_sso_and_budgets.py`, `test_auto_budgets.py`, `test_limits_auto.py`, `test_budget_review_fixes.py`, `test_cost_reservations.py`, `test_reservation_resolvable.py`, `test_person_allowance.py`, `test_drift_guards.py` (spend); `test_idle_minds.py` (spend is not input, with the `port/idle-minds` pull request).

## Swap point
**Yes**, the ledger. A replacement must answer `check` before dispatch with worst-case cost, keep reservations durable across a crash, and settle or expire every hold. Conformance test: none yet, write one first.

## Equivalent in the SingularityNET stack
Option to evaluate: an AGIX/FET settlement adapter on the spend ledger, which the federation road names as its last step (`docs/theory/ledger-provenance-and-das.md:130-134`); marketplace payment channels for paid services.

## Keep criteria
Keep if a crash test between reserve and settle never loses or double-counts a hold, and the Limits page matches what admission enforces.

## Read next
[05-governance/02-budgets-and-spend](../05-governance/02-budgets-and-spend.md), [01-system/03-state-and-storage](../01-system/03-state-and-storage.md), [03-minds/05-models-and-gateway](../03-minds/05-models-and-gateway.md), [08-reviewers/02-invariants, I-G](../08-reviewers/02-invariants.md#i-g-spend-and-models), [08-reviewers/03-review-checklists, spend](../08-reviewers/03-review-checklists.md#4-models-gateway-and-spend), [10-testing/03-gaps](../10-testing/03-gaps.md).
