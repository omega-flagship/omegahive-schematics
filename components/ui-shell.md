# UI shell and experiences
> Seam-register card. Code refs are to `omegahive` @ 34b0fb3 unless another repo is named. Back to the [register](README.md).

## What it does
The web UI (React and TypeScript in `hive/ui`). The shell gives navigation, the Ask on every page, and per-person looks (colour and font tokens, layout, density). Experiences are whole alternative front ends over the same hive (Classic, Professional, Cosmos, Construct, Still, Flux, Canvas, and the closed-tier OmegaTown). Classic pages still open over any experience.

Upstream: [web stack](https://github.com/PhysixSNET/omegahive-start-here/blob/main/ACKNOWLEDGEMENTS.md#web-stack), [MeTTa and Hyperon](https://github.com/PhysixSNET/omegahive-start-here/blob/main/ACKNOWLEDGEMENTS.md#metta-and-hyperon).

## Where it lives
- `hive/ui/src/App.tsx` (417 lines; `ExperienceHost` `:185`, `AskHost` `:390`).
- `hive/ui/src/experiences/registry.ts`: `ExperienceDef` `:10-28`, `CLASSIC` `:30`, list `:65-131`, `offeredExperiences` `:142`, only reviewed experiences in production builds (`:24-27`).
- `hive/ui/src/shell/` (`Nav.tsx`, `uiVariant.ts`, `appLook.ts`, `layout.ts`); feature pages `hive/ui/src/features/*`.
- Server side: `hive/core/ui_prefs.py:165` `UiPrefs` (looks are data only, `:1-5`); routes `GET|PUT|DELETE /api/me/ui` (`hive/core/app.py:910-936`); UI served by a catch-all that never answers `api`, `llm` or `agent-hub` paths (`app.py:3380-3392`).
- Closed tier: `hive/ui/src/experiences/omegatown` (`docs/MODULARITY.md:20`).

## Contract at its edge
- **Experience:** an `ExperienceDef` `{id, name, tagline, blurb, companionLook?, swatch, load?, reviewed?}` registered in `registry.ts`.
- **Look:** a `UiVariant` of allow-listed tokens; no CSS text, URLs or scripts (`ui_prefs.py:3-5`); checked by `blockedReason` (`shell/uiVariant.ts:88`).
- **Data:** REST (`hive/ui/src/api/`) and the live events socket ([events](events.md)).

## Status and known issues
**Partial.** Built; the full "any UI" reshaping is mostly finished and untested (`STATUS.md:72`). The demo mode was listed as out of date and broken (`STATUS.md:77`); the live fixes since the handover snapshot (blocked browser storage, guided-demo marks and folding, `?tab=commons`, a guarded `?view=graph`, one approval card at a time, the ticker above the Ask) arrive with the omegahive pull requests `port/demo-mode-fix` and `port/surface-followups-r4`, which close that known issue. Chat labels now say "You" only for the viewer's own messages ([UI page](../02-ask-and-ui/02-ui-experiences-and-looks.md#how-it-works)). A few UI tests time out under load (`STATUS.md:78`).

## Tests that guard it
UI: `npx vitest run` in `hive/ui` (for example `experiences/*.test.ts`, `shell/*.test.ts`, `wordingGuard.test.ts`, `privateNames.test.ts`); types `npx tsc -b --noEmit`. Hive: `hive/tests/test_ui_prefs.py`.

## Swap point
**Yes.** A new experience registers in `registry.ts` and must be reviewed before production builds offer it. A whole new front end can use the same REST and events API. Conformance test: `experiences/registry.test.ts` for registration; none yet for API parity.

## Equivalent in the SingularityNET stack
No direct equivalent. The browser already runs MeTTaScript for the personal mind (`hive/ui/src/lib/mindSpace/core.ts:1-6`).

## Keep criteria
Keep if the map shows nothing a viewer may not see (one visibility helper before any grouping), Health's actions follow only the host's flags, the production build offers only reviewed experiences, the Ask works in each one, and the demo mode, now fixed, is re-checked on the launch build (or removed).

## Read next
[02-ask-and-ui/02-ui-experiences-and-looks](../02-ask-and-ui/02-ui-experiences-and-looks.md), [02-ask-and-ui/01-ask-and-conductor](../02-ask-and-ui/01-ask-and-conductor.md), [07-upgrade-path/02-swap-seams, UI shell](../07-upgrade-path/02-swap-seams.md#12-the-ui-shell), [08-reviewers/02-invariants, I-U](../08-reviewers/02-invariants.md#i-u-ui), [08-reviewers/03-review-checklists, UI](../08-reviewers/03-review-checklists.md#10-ui-experiences-and-the-app-frame).
