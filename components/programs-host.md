# Programs host and contract
> Seam-register card. Code refs are to `omegahive` @ 34b0fb3 unless another repo is named. Back to the [register](README.md).

## What it does
Loads apps (dot programs) into the hive process. An app is a folder with `plugin.json` and a Python module that defines `describe()`, `view()` and `act()`. It supplies a work graph; the host draws it in four stages (unfold, map, compare, detail). People act through host confirm; minds may use only actions the app marks for agents. Apps get a narrow `ProgramContext` to reach the hive.

## Where it lives
- `hive/core/programs.py:1-7` (contract summary), `CONTRACT = "0.1"` `:33`, `ProgramContext` `:97`, `Programs` `:347`; discovery `:507`; load with `importlib` `:673-675`; `reload` `:534`; `view` `:992`; `act` `:1053`; `validate_graph` `:1227`.
- `hive/core/program_actions.py:86` `ProgramActions`: `agent_act` `:130`, `person_act` `:381`, `mint_confirm` `:311`.
- `hive/core/program_attachments.py:1`, `hive/core/app_drafts.py:1`, `hive/core/sandbox_run.py:1`.
- The written contract: `hive/PROGRAMS.md` (signatures §1, shapes §2, actions §3, mounting §4, permissions §5, compatibility test §6, HTTP routes §8, frame bridge §9).
- Built-in apps: `hive/plugins/` (`commons_explorer`, `contract_fixture`; `omegaevolve` is closed tier).

## Contract at its edge
- **Python:** `describe()`, `view(ctx, focus, stage)`, `act(ctx, action, items, params)`; the hive sets `ctx.actor` and `ctx.command` for `act` (contract 0.2 fields, `programs.py:100-102`).
- **Routes:** `GET /api/programs`, `POST /api/programs/{id}/view`, `/read`, `/act`, `/confirm`, activations, offers, attachments (`hive/core/app.py:2820-2964`); minds `POST /api/agent/programs/{id}/act` (`:3358`).
- **Settings:** `HIVE_PLUGIN_DIRS` (extra app folders), `HIVE_APP_HOMES`, `HIVE_APP_GRANT_RENEWAL`, per-app swarm settings.

## Status and known issues
**Built**, v0.1 frozen. `STATUS.md:39-41`. `act` already uses two v0.2 fields while FEATURES lists v0.2 as planned (`docs/FEATURES.md:216`). Apps run in the hive process; out-of-process apps are planned. No single flow deploys an app with its swarm (`STATUS.md:67`).

## Tests that guard it
`hive/tests/test_programs_api.py`, `test_program_actions.py`, `test_program_confirm.py`, `test_program_homes.py`, `test_program_read.py`, `test_program_refusal.py`, `test_app_seams.py`, `test_app_attachments.py`, `test_app_drafts.py`, `test_read_actions.py`, `test_scientist_route.py`, `test_programs_check_async.py`.

## Swap point
**Yes.** This is the main plug-in seam. A new or replacement app must pass the offline checker: `python -m hive.programs_check path/to/program_dir` (`hive/programs_check.py:1-5`).

## Equivalent in the SingularityNET stack
Option to evaluate: offering an app as a SingularityNET marketplace service and wrapping it in a thin program that calls it. The contract itself is plain JSON with no MeTTa dependency (`hive/PROGRAMS.md:11`).

## Keep criteria
Keep if `programs_check` runs in CI on every app release, and the team decides whether in-process loading is acceptable for launch or out-of-process apps come first.

## Read next
[06-apps/01-programs-contract](../06-apps/01-programs-contract.md), [06-apps/02-app-lifecycle](../06-apps/02-app-lifecycle.md), [06-apps/03-connect-a-new-app](../06-apps/03-connect-a-new-app.md), [07-upgrade-path/02-swap-seams, apps contract](../07-upgrade-path/02-swap-seams.md#10-the-apps-contract-v02-out-of-process), 09-security-and-launch/01-threat-model, TB3 (in the private omegahive-security repo; ask Kabir), [08-reviewers/02-invariants, I-AP](../08-reviewers/02-invariants.md#i-ap-apps), [08-reviewers/03-review-checklists, apps](../08-reviewers/03-review-checklists.md#9-apps-and-the-programs-contract).
