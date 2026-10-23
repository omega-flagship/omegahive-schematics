# People and auth
> Seam-register card. Code refs are to `omegahive` @ 34b0fb3 unless another repo is named. Back to the [register](README.md).

## What it does
Decides who a request comes from. People sign in with the admin password or with invite-only Google sign-in; an optional companion webhost can also vouch for a person. A public gate marks requests that arrive through a proxy or base path and keeps them away from mind-only routes.

## Where it lives
- `hive/core/people.py:141` `People`: invites, Google sign-in, roles; `revoke_sessions` at `:236`; domain allowlist `signin_domains` at `:108`; configured admins `admin_emails` at `:97`.
- `hive/core/sso.py:30` `SSO` (companion webhost cookie) and `hive/core/sso.py:86` `PublicGate` (ASGI middleware). Mind-only path prefixes: `hive/core/sso.py:26`.
- Routes in `hive/core/app.py`: login `:347`, methods `:357`, Google start and callback `:382,389`, invites `:412,760,771`, people `:755,776`, SSO `:783`, logout `:831`, me `:847`.

## Contract at its edge
- **Routes:** `POST /api/auth/login` returns a bearer token; `GET /api/auth/me`; `POST /api/auth/logout` ends every token from that sign-in.
- **Settings:** `HIVE_ADMIN_PASSWORD`, `HIVE_GOOGLE_CLIENT_ID`, `HIVE_GOOGLE_CLIENT_SECRET`, `HIVE_GOOGLE_REDIRECT_URI` (`people.py:156-158`), `HIVE_SIGNIN_DOMAINS`, `HIVE_ADMIN_EMAILS`, `HIVE_SSO_TTL_HOURS` (`people.py:159`), `HIVE_SSO_USERS`, `HIVE_PUBLIC_PASSWORD` (`sso.py:35-38`), `HIVE_BASE_PATH`.
- **Invariant:** public requests never reach `/agent-hub`, `/llm/` or `/api/agent/` (`sso.py:26`).
- **Output to the rest of the hive:** a session with a principal and a role. Every other card trusts this.

## Status and known issues
**Built.** `STATUS.md:26-27`. After any restart, check that Google sign-in is ready (`People.google_ready`, `people.py:197`), not only that the server answers.

## Tests that guard it
`hive/tests/test_people_api.py` (41 tests, Google faked), `test_sso_and_budgets.py`, `test_settings.py`, `test_person_session_ref.py`.

## Swap point
**Yes.** A replacement identity provider must yield the same session shape (principal, role, signed-in method) and keep the public-gate invariant. Conformance test: none yet, write one first. Start from `test_people_api.py` and `test_sso_and_budgets.py`.

## Equivalent in the SingularityNET stack
No direct equivalent in the Hyperon stack. Options to evaluate: wallet-based or decentralised identity from the ASI:Chain work, once it is ready, as an extra sign-in method beside Google.

## Keep criteria
Keep as is if the team accepts Google plus a password for launch, the public-gate rule passes a review against every agent route, and token revocation on sign-out is shown in a test.

## Read next
[01-system/04-request-lifecycle](../01-system/04-request-lifecycle.md), [05-governance/01-permissions-and-policy](../05-governance/01-permissions-and-policy.md), [05-governance/04-isolation](../05-governance/04-isolation.md), 09-security-and-launch/01-threat-model, TB1 (in the private omegahive-security repo; ask Kabir), [08-reviewers/02-invariants, I-D](../08-reviewers/02-invariants.md#i-d-front-door-and-routes), 09-security-and-launch/02-launch-readiness-checklist, security (in the private omegahive-security repo; ask Kabir), [10-testing/04-e2e-scenarios, scenario 2](../10-testing/04-e2e-scenarios.md#2-public-boundary-through-a-real-proxy).
