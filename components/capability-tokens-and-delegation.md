# Capability tokens and delegation
> Seam-register card. Code refs are to `omegahive` @ 34b0fb3 unless another repo is named. Back to the [register](README.md).

## What it does
Two kinds of bounded authority. **Capability tokens** let a registered service (the Code service is the first) act for one actor, on one task, for named actions and paths, until expiry; the service checks live status before each change. **Delegation leases** let a coordinating mind start and stop a member for one task, for at most 15 minutes and within a budget, under a lease a named admin issues.

## Where it lives
- `hive/core/services.py:1-17` (token format and claims), `:104` `Services`: `enrol` `:119`, `register` `:129`, `issue` `:231`, signature `:309-310`, `capability_status` `:312`, `redeem` `:363`; action sets `:32-47`.
- `hive/core/delegation.py:1-12` (rules), `:64` `Delegation`; sandbox required `:108`.
- `hive/core/lifecycle_broker.py:13` `LifecycleBroker` (`issue` `:35`, `valid` `:68`, `reconcile` `:116`), adopted from a closed-tier repo.
- Routes: services `hive/core/app.py:426-468`, approvals redeem `:576-591`, goal grants `:597-615`, lifecycle `:3124-3140`.

## Contract at its edge
- **Token:** `hc1.<base64url claims>.<HMAC-SHA256 hex>`; claims `{id, iss, aud, actor, kind, task_id, swarm_id, repository_id, actions[], paths, argv_prefixes, exp, iat, max_runs, max_runtime_seconds, member_hash, grant_id}` (`services.py:8-11`).
- **Live check:** `GET /api/services/capabilities/{id}` before every mutation; revoke with `DELETE` (`app.py:464-468`).
- **Approvals for `code-*` skills:** redeemed once for the exact binding, `POST /api/agent/approvals/{id}/redeem` (`services.py:15-17`).
- **Lease:** `POST /api/lifecycle/leases` (admin), then `POST /api/agent/lifecycle/{action}` (coordinator).

## Status and known issues
**Built.** `STATUS.md:36`. Delegated specialists start only when `HIVE_MIND_SANDBOX=1` and OS isolation is available (`delegation.py:108`). Copy-apply purpose tokens are built, but the feature is off (`STATUS.md:57`).

## Tests that guard it
`hive/tests/test_services_api.py`, `test_connection_services.py`, `test_grant_scope.py`, `test_app_grant_renewal.py`, `test_delegation.py`, `test_copy_apply_claims.py`, `test_copy_apply_consent.py`, `test_proposal_tests.py`.

## Swap point
**Yes**, the token format, if every verifier changes with it. A replacement must keep per-actor, per-task scoping, short expiry, live revocation, and single-use approvals. Conformance test: none yet, write one first.

## Equivalent in the SingularityNET stack
Options to evaluate: signed tokens tied to a per-hive key (the federation road's step 2, `docs/theory/ledger-provenance-and-das.md:120-122`); on-chain multisig for governance-critical leases later.

## Keep criteria
Keep if the capability secret is rotatable, every service verifies both signature and live status, and a crashed coordinator never leaves a specialist running (reconcile test).

## Read next
[05-governance/01-permissions-and-policy](../05-governance/01-permissions-and-policy.md), [05-governance/04-isolation](../05-governance/04-isolation.md), [code proxy](code-proxy.md), 09-security-and-launch/01-threat-model, TB5 (in the private omegahive-security repo; ask Kabir), [08-reviewers/03-review-checklists, policy](../08-reviewers/03-review-checklists.md#3-policy-approvals-and-capabilities), 09-security-and-launch/02-launch-readiness-checklist, governance (in the private omegahive-security repo; ask Kabir).
