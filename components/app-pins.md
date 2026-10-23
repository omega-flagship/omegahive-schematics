# App pins
> Seam-register card. Code refs are to `omegahive` @ 34b0fb3 unless another repo is named. Back to the [register](README.md).

## What it does
Makes the hive load only the exact release of each app that was reviewed. A pin names an app's release folder and the sha256 digest of its sources (and optionally of named files and environment values). If the folder on disk differs, the app is refused. Updates show what is waiting to load and apply it under holds.

## Where it lives
- `hive/core/programs.py:593-660` (pins: read, refusal reasons, folder versus pin); `source_digest` `:547`; `PIN_REFUSALS` `:22`; recheck on open `:745-746`, `:837-860`.
- `hive/core/updates.py:45` `Updates` (what is waiting, holds, apply).
- Routes: `GET /api/updates`, `POST /api/updates/requests`, `/holds`, `/apply`, mind side `/api/agent/updates*` (`hive/core/app.py:1377-1412`).

## Contract at its edge
- **Setting:** `HIVE_APP_PINS` is a JSON object `{program_id: {release: <absolute path>, digest: "sha256:<64 hex>", files?: {relpath: digest}, env?: {...}}}` (`programs.py:636`). `HIVE_APP_PINS_REQUIRED=1` refuses any unpinned non-built-in app (`programs.py:602,618`).
- **Refusals:** `release_mismatch`, `duplicate_discovery`, `pin_conflict`, `unpinned`, `pins_invalid` (`programs.py:22`); an app UI that fails its lock is closed with 403 `app_integrity`.
- **Rule:** a running app can write the environment, so a reload never re-reads `HIVE_APP_PINS` for itself (`programs.py:582`).

## Status and known issues
**Built.** `STATUS.md:39`. Pins, swarm settings, homes and grants are set in separate places with no check that they agree (`STATUS.md:67`). Services must load releases, not owners' working folders.

## Tests that guard it
`hive/tests/test_app_pins.py`, `test_updates.py`, `test_app_ui_parts.py`.

## Swap point
**Yes**, the source of trust. A replacement (signed releases, a registry) must still refuse any byte change and fail closed when pins are required. Conformance test: `hive/tests/test_app_pins.py` is the closest; none yet for a new backend.

## Equivalent in the SingularityNET stack
Option to evaluate: signing pin sets with a per-hive key and anchoring them on ASI:Chain later (`docs/theory/ledger-provenance-and-das.md:120-122`).

## Keep criteria
Keep if `HIVE_APP_PINS_REQUIRED=1` is on for launch, and one guided step sets pin, swarm, home and grants together.

## Read next
[06-apps/02-app-lifecycle](../06-apps/02-app-lifecycle.md), [06-apps/03-connect-a-new-app](../06-apps/03-connect-a-new-app.md), 09-security-and-launch/01-threat-model, TB3 (in the private omegahive-security repo; ask Kabir), [08-reviewers/03-review-checklists, apps](../08-reviewers/03-review-checklists.md#9-apps-and-the-programs-contract), 09-security-and-launch/02-launch-readiness-checklist (in the private omegahive-security repo; ask Kabir).
