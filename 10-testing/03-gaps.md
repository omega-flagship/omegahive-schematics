# Testing gaps
> Code refs are to omegahive @ 34b0fb3 unless named. Counts come from each repository's `STATUS.md` (2026-10-10).

**What this shows.** What the green numbers on [02-how-to-run.md](02-how-to-run.md) do not prove. Read it before you call anything "tested". The scenarios that close the biggest gaps first are on [04-e2e-scenarios.md](04-e2e-scenarios.md).

**Who should read it.** Whoever signs off a launch, and every component owner. The launch checklist items these gaps feed are TST3 to TST8 in the checklist (in the private omegahive-security repo; ask Kabir).

## The short version

Thousands of unit and integration tests pass. Very little has been tested end to end, on Linux, in a browser, or on the CI platform the repository will live on. `STATUS.md` says it plainly: "Everything here has worked in one or another earlier build, but these pieces have only lived together for about a week. Expect integration bugs" (`STATUS.md:74`).

## Gaps

| # | Gap | Evidence | What it means | Checklist |
|---|---|---|---|---|
| G1 | **Limited end-to-end testing** across features | `STATUS.md:74` | Each part is tested on its own, mostly in one process with fakes. Flows that cross the browser, the hive, a real mind, the Code service and an app are largely untested together | TST5 |
| G2 | **Real-mind tests are opt-in** | the three acceptance files skip unless `HIVE_E2E=1` (`hive/tests/test_acceptance.py:22`) | The default hive run, and CI, never start a real native mind. Restart survival of the commons is proven only there | TST5 |
| G3 | **No browser end-to-end** | vitest runs in `node` (`hive/ui/vite.config.ts:20-23`); the one Chromium test skips without a browser (`hive/ui/src/lib/appFrame.browser.test.ts:10`); app repos report the same: the Atlas frontend smoke not run, Fusion "Browser acceptance ... is not part of these tests", Studio "no browser test", Purple "Browser appearance has not been verified" (each repo's `STATUS.md`) | Nothing checks that the real UI renders and works against a real hive | TST6 |
| G4 | ~~CI has never run on GitHub~~ **Closed** | CI now runs on GitHub Actions on every push and pull request, with three blocking jobs on `ubuntu-24.04`: `core-tests` (`tests/`, unittest), `hive-petta` (the pinned toolchain, then `hive/tests`, with unprivileged user namespaces enabled for the Linux mind sandbox) and `hive-ui` (typecheck, lint, vitest, build) (`.github/workflows/ci.yml:1-15`, `:66-69`). The first run passed core-tests and hive-ui and 2402 hive tests; its 19 failures (the Linux sandbox tests, and one SQLite default) were fixed in omegahive PR #3, and all three jobs now pass | Whether CI is required for merge (branch protection) is not recorded here | TST3 |
| G5 | **Linux is unproven for the frontier features** | computer use, browser use, draw on screen and vibe coding are "tested working on the Mac and unproven on Linux" (`STATUS.md:70`) | The cloud target is Linux. These features have no Linux evidence | TST7 |
| G6 | **The release counts do not name a platform; Linux isolation tests skip elsewhere** | `STATUS.md:9-11`; Linux tests need Landlock and user namespaces (skip reasons in `hive/tests/test_mind_sandbox_linux.py`); the last recorded full Linux run was at an earlier release (release report, "Linux test suite") | A green run on a Mac does not exercise the Linux sandbox at all | TST4 |
| G7 | **No mind has been observed running on Linux in the release** | release report, "Not yet observed: ... any mind running on Linux"; "SHADOW EVIDENCE: none for minds" | The Linux isolation probes passed, but a real mind working inside it at this release has not been watched | TST4 |
| G8 | **V2 tests need the runtime bundle** | omegav2: 478 collected, 184 passed, 212 failed, 78 errors; 192 of the 290 are `runtime-bundle-absent`, the rest need inputs from the owner's private archive; treated as UNKNOWN (omegav2 `STATUS.md`) | The V2 body's suite cannot be judged from the handover alone | |
| G9 | **Owner-workspace dependencies** | omegacode: 62 owner-layout tests need unpublished toolchains, TypeScript tests hard-code a Node path; Fusion and Social qualification runners need the owner's layout; candidate host probes not run (each repo's `STATUS.md`) | Some tests that matter most for integration cannot be run from the published repos | TST8 |
| G10 | **App counts were measured against prep commits** | apps name omegahive `7b1ce3f` or `e4571e9`, not `34b0fb3` (each repo's `STATUS.md`) | Re-run every app suite against the release commit | TST8 |
| G11 | **Outside services are never called** | no test calls a real model provider; Google sign-in is not run end to end; Docker tests need a daemon and an image (skip reasons) | Provider error shapes, OAuth redirects and real container behaviour are untested | |
| G12 | **Modules, channels and add-ons are not ported** | "known to work in previous builds, but their compatibility with this hive is untested" (`STATUS.md:76`) | Their unit tests in `tests/` do not show they work with the current hive | |
| G13 | **MeTTa smokes and Autotests are outside CI** | CI runs `hive/tests`, `tests/` (unittest) and the UI only (`ci.yml:1-11`); Autotests are legacy (`Autotests/LEGACY.md:3`) | No recorded counts for either | TST3 |
| G14 | **Green tests, broken demo** (closing) | the UI suite passed apart from timeouts (`STATUS.md:18`), while the demo mode was "out of date and broken" (`STATUS.md:77`). The live demo fixes since the handover snapshot (omegahive pull requests `port/demo-mode-fix` and `port/surface-followups-r4`) add route and guard tests: `tour/scriptRoutes.test.ts`, `features/swarm/commonsView.test.ts`, `features/programs/viewLink.test.ts`, `features/setup/checklist.test.ts`, `api/sim/coordinatorAwake.test.ts` | The demo still has no browser end-to-end run (TST6); re-check it by hand on the launch build | |
| G15 | **Reasoning and child minds not exercised live** | automatic reasoning deliberately not wired; reasoning tools "not activated or bug-fixed in this build"; child minds "never spawned live" (`STATUS.md:49`, `:53`, `:73`) | Their tests prove the held code, not live behaviour | |
| G16 | **Known code paths without a test** | `HIVE_ALLOW_UNPRICED=1` chat path (see [models and gateway](../03-minds/05-models-and-gateway.md)); quarantine reachable only in `tests/hive_lib_smoke.metta` (K3); out-of-range f or c over REST not run (K5); no test pins the `LOCAL_ALLOW` list (`modules/hive/src/hive_commons.py:931-936`) | Behaviour here is read from the code, not observed | |
| G17 | **No operational tests** | no backup and restore drill, no upgrade or data migration test, no load or soak test of the hive (none found in `hive/tests`) | Operations are documented (`deploy/RUNBOOK.md` §8) but not exercised | DAT3, OPS8 |
| G18 | **Flaky under load** | 5 UI tests time out at 5 seconds on a loaded machine (`STATUS.md:78`) | A red UI run may be load, not a defect; a slow CI runner may hit it | |
| G19 | **A skip can hide a whole platform** | 66 hive skips; Linux, macOS, Docker, `HIVE_E2E` and sibling-repo skips all count as "not failed" | Read the `-rs` summary, not just the totals | |

## For reviewers: what to check

- **Bind every claim to the command that produced it.** "2414 passed" proves what `python -m pytest -q hive/tests` exercised on that machine, with those skips. It does not prove Linux isolation, a real mind, or the UI in a browser.
- **Platform first.** Re-run on the launch OS at the release commit before quoting a count.
- **Close a gap with a scenario.** Each gap above should end in a test that runs by default, or in a written acceptance of the risk.

## References

- `STATUS.md:9-18`, `:49-78`
- `hive/tests/test_acceptance.py:1-22`
- `hive/ui/vite.config.ts:20-23`; `hive/ui/src/lib/appFrame.browser.test.ts:1-25`
- `.github/workflows/ci.yml:1-27`
- `Autotests/LEGACY.md:1-3`
- `docs/handoff/platform/release-report-2026-10-06.md` ("Linux test suite", "Not yet observed")
- Each app repo's `STATUS.md` (2026-10-10)
