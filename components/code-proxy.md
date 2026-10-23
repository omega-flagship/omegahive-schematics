# Code proxy
> Seam-register card. Code refs are to `omegahive` @ 34b0fb3 unless another repo is named. Back to the [register](README.md).

## What it does
Lets people and minds edit the code of anything running in the hive. Opening an edit target creates a task with an edit grant. The browser talks only to the hive; the hive forwards a small allow-list of routes to the separate Code service (closed tier, `omegacode`) with a short-lived signed capability, never a service secret.

## Where it lives
- `hive/core/code.py:1-9` (contract), `:270` `Code`: `targets` `:331`, `open` `:430`, `attach` `:447`, `select_target` `:476`, `require_intended_release` `:596`, `proxy` `:605`.
- Allow-list `PROXY_ROUTES` `code.py:62`; the release the routes were written for `INTENDED_SERVICE_RELEASE` `:47`; copy-apply routes held `:178-215`.
- Routes: `hive/core/app.py:509-531` (capabilities), `:708-750` (targets, open, attach, select, proxy).
- Tokens: [capability tokens and delegation](capability-tokens-and-delegation.md).

## Contract at its edge
- **Route:** `GET|POST /api/code/proxy/{path}` with `task_id`, `grant_id`, `repository_id` (admin session, `app.py:743-752`).
- **Refusals:** 404 `not_relayed` (route not on the list, or held), 403 `purpose_only`, 503 `service_release_mismatch`.
- **Settings:** `HIVE_CODE_OWNERS`, `HIVE_CODE_REPOS`, `HIVE_CODE_ALLOW_PRIVATE`, `HIVE_CODE_SERVICE_CONFIG`, `HIVE_COPY_APPLY_CLAIMS` (`code.py:275-300`).
- **Service side:** the Code service's own owner contract (in its repo's `docs/schematics/`).

## Status and known issues
**Partial.** Live on one owner hive; the cloud install is in review (`STATUS.md:58`). Copy-apply is off (`STATUS.md:57`).

## Tests that guard it
`hive/tests/test_code_api.py`, `test_code_proxy_actions.py`, `test_code_module.py`, `test_code_*_skills.py`, `test_grant_scope.py`, `test_copy_apply_*.py`.

## Swap point
**Yes.** Another code service can sit behind the proxy if it registers as a service, verifies `hc1` capabilities and live status, and serves the allow-listed routes. Conformance test: none yet, write one first.

## Equivalent in the SingularityNET stack
No direct equivalent known to this author.

## Keep criteria
Keep if the service release check runs on every rollout, and the allow-list is reviewed against the service's routes each release.

## Read next
[06-apps/03-connect-a-new-app](../06-apps/03-connect-a-new-app.md), [05-governance/01-permissions-and-policy](../05-governance/01-permissions-and-policy.md), 09-security-and-launch/01-threat-model, TB5 (in the private omegahive-security repo; ask Kabir), 09-security-and-launch/02-launch-readiness-checklist, isolation (in the private omegahive-security repo; ask Kabir), [10-testing/01-test-map](../10-testing/01-test-map.md#components-and-their-tests).
