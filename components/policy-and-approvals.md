# Policy and approvals
> Seam-register card. Code refs are to `omegahive` @ 34b0fb3 unless another repo is named. Back to the [register](README.md).

## What it does
Decides, when a mind asks it about a skill, whether the skill is allowed, waits for a person, or is refused. The most specific matching rule wins (mind, then swarm, then hive; an exact name beats a glob). `ask` files an approval; a person answers Once, For a time, Always, No or Never, and an approved command runs once for that exact binding.

The gate does **not** yet see every skill. Two bypasses are built today:
- **Local skip list.** A native mind's loop runs the skills in `LOCAL_ALLOW` without asking the gate at all: `send`, `send-hive-to`, `wait`, `pin`, `query`, `remember`, `episodes`, `hive-publish`, `hive-query`, `hive-belief`, `hive-goals`, `hive-goal-claim`, `hive-goal-done`, `hive-goal-fail`, `hive-goal-create`, `hive-shares` and `hive-revision-part` (`modules/hive/src/hive_commons.py:932-956`). A deny or ask rule on these is never consulted for that loop (K10).
- **Unknown skills default to allow.** A skill that matches no rule and no default list is allowed (`hive/core/policy.py:219`), so a new side-effecting module skill runs unless its owner adds an ask rule (K30).

Universal gating is a launch requirement (K10, K30); see FINDINGS.md (in the private omegahive-security repo; ask Kabir) and 03-hardening-for-launch.md (in the private omegahive-security repo; ask Kabir).


## Where it lives
- `hive/core/policy.py:1-8` (contract), `:120` `Policy`: `decide` `:181`, `authorize` `:237`, `enforce` `:290`, `answer` `:350`, `decide_approval` `:381`.
- Default lists: `HUMAN_ONLY` `:48`, `DEFAULT_ALLOW` `:50`, `DEFAULT_ASK` `:55`, `HIGH_RISK` `:62`; reviewed hive skills `REVIEWED_HIVE_SKILLS` `:27`; exact-only skills `EXPLICIT_ONLY` `:21`.
- App-action decisions: `hive/core/program_actions.py:233` `decide`.
- Routes: rules `hive/core/app.py:2259-2270`, approvals `:2275-2306`, mind-side `POST /api/agent/authorize` `:2679` and `/api/agent/skills/decisions` `:2685`.

## Contract at its edge
- **Mind call:** `POST /api/agent/authorize` with the canonical command; answer `{decision: allow|ask|deny, message}`.
- **Rule:** `(scope, skill pattern, mode, note, expires_at)`, mode `allow`, `ask` or `deny` (`policy.py:132-133`).
- **Approval answer:** `POST /api/approvals/{id}/decide` with the five-way choice; `track-record` shows earlier answers (`app.py:2290`).
- **Defaults:** human-only skills are always refused; a new `hive-*` skill defaults to `ask` until reviewed (`policy.py:184,214`).

## Status and known issues
**Built.** `STATUS.md:35-36`. One signer per approval and two risk levels (`STATUS.md:56`). Multi-signer approvals are intended (`docs/theory/ledger-provenance-and-das.md:94-97`).

## Tests that guard it
`hive/tests/test_phase2_api.py`, `test_policy_hive_skills.py`, `test_five_way_decisions.py`, `test_sensitive_action_revalidation.py`, `test_program_actions.py`, `test_program_confirm.py`.

## Swap point
**Yes**, the decision engine. A replacement must answer `authorize` for every skill before it runs, keep human-only refusals unconditional, and bind an approval to one exact command. Conformance test: none yet, write one first; `test_five_way_decisions.py` and `test_policy_hive_skills.py` cover the current rules.

## Equivalent in the SingularityNET stack
Options to evaluate: policy rules and approvals as atoms (the V2 governance draft names `ApprovalReceipt` and `QuorumReceipt`, `docs/theory/ledger-provenance-and-das.md:108-111`), with on-chain multisig as a later recorder, never the authoriser.

## Keep criteria
Keep if every effect path (skills, app actions, Code, MCP tools) is shown to pass through `authorize` or `decide`, and approvals cannot be replayed for a changed binding.

## Read next
[05-governance/01-permissions-and-policy](../05-governance/01-permissions-and-policy.md), [05-governance/05-intended-governance](../05-governance/05-intended-governance.md), [07-upgrade-path/02-swap-seams, policy engine](../07-upgrade-path/02-swap-seams.md#8-the-policy-engine), 07-upgrade-path/03-hardening-for-launch (in the private omegahive-security repo; ask Kabir), [08-reviewers/02-invariants, I-A](../08-reviewers/02-invariants.md#i-a-governance), [08-reviewers/03-review-checklists, policy](../08-reviewers/03-review-checklists.md#3-policy-approvals-and-capabilities), [10-testing/04-e2e-scenarios, scenario 4](../10-testing/04-e2e-scenarios.md#4-approval-round-trip-in-the-browser).
