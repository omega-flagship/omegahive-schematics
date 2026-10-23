# Visibility
> Seam-register card. Code refs are to `omegahive` @ 34b0fb3 unless another repo is named. Back to the [register](README.md).

## What it does
Decides what each person may see. Minds and swarms are private, shared or public; admins keep sight for audit. Other people's personal minds are hidden from default lists. The same rules filter live events.

## Where it lives
- `hive/core/visibility.py:270` `Visibility`; `Viewer.sees` at `:205-210`.
- Path and name checks: `check_path` `:299`, `check_named_minds` `:281`.
- Personal-mind hiding: `hidden_personal` `:312`, `hide_others_personal` `:343`.
- Event filter: `EVENT_RULES` `:232`, `event_rule` `:262`, `event_visible` `:499`.
- Setting it: `Visibility.set` `:559`; routes `PUT /api/agents/{id}/visibility` and `PUT /api/swarms/{id}/visibility` (`hive/core/app.py:1257,1268`).

## Contract at its edge
- **Values:** `visibility` is `private`, `shared` or `public`, with a `shared_with` list (`visibility.py:193` `clean`).
- **Rule for owners:** every list and read route passes its rows through `hive.visibility`; every new event kind needs an `EVENT_RULES` entry, or members never receive it.
- **Consumers:** every route in `app.py`, the motivations routes (`hive/core/motivations.py:154` `readable`), the events socket (`app.py:1941`).

## Status and known issues
**Built.** `STATUS.md:35-38`. Coverage depends on every route calling it; there is one shared layer but no single enforcement point yet (`docs/MODULARITY.md:43-44`). Live since the handover snapshot (the omegahive pull request `port/idle-minds`): a personal mind's conversations are its person's, the loopback operator included, and Health's idle question goes to the person's own chat ([visibility page](../05-governance/03-visibility-and-privacy.md#how-it-works)). The two gaps found then (K65, K66) are fixed by the omegahive pull request `port/idle-minds-r2.5`: a personal mind's idle record and export follow the person's transcript or an explicit audit whatever its visibility, and agent views carry per-viewer flags `is_mine`, `may_remind`, `may_sleep`.

## Tests that guard it
`hive/tests/test_visibility.py` (includes `test_every_published_event_kind_has_a_rule`), `test_personal_visibility.py`, `test_share_visibility.py`, `test_focus_visibility.py`, `test_request_visibility.py`, `test_archive_visibility.py`; `test_idle_minds.py` (personal-mind conversations and the idle routes, with the `port/idle-minds` pull request).

## Swap point
**No.** It is a cross-cutting rule, not a module behind a contract. A replacement would have to be called from every route. Conformance test: none yet, write one first (an inventory test that every list route filters).

## Equivalent in the SingularityNET stack
Option to evaluate: per-pattern access grants in the style of the DAS `AuthorizationManifest`, which the federation design already names (`docs/theory/ledger-provenance-and-das.md:84-91`).

## Keep criteria
Keep if a route inventory shows every list and read route filtered, and the event-rule test stays green.

## Read next
[05-governance/03-visibility-and-privacy](../05-governance/03-visibility-and-privacy.md), [01-system/02-hive-server-map](../01-system/02-hive-server-map.md), [08-reviewers/02-invariants, I-V](../08-reviewers/02-invariants.md#i-v-visibility-and-privacy), [08-reviewers/03-review-checklists, privacy](../08-reviewers/03-review-checklists.md#2-visibility-and-personal-privacy), 09-security-and-launch/02-launch-readiness-checklist, privacy (in the private omegahive-security repo; ask Kabir).
