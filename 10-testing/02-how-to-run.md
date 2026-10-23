# How to run each suite
> Counts are copied from each repository's `STATUS.md` as handed over on 2026-10-10. They were not re-run for this page. Code refs are to omegahive @ 34b0fb3 unless named.

**What this shows.** The exact toolchain, the command for each suite, and the last recorded result. Which component each suite covers is on [01-test-map.md](01-test-map.md).

**Who should read it.** Anyone setting up a development machine or a CI runner, and anyone checking whether a green result means what it seems to mean.

## The toolchain

The same pins appear in the README, the CI file and both setup scripts (`README.md:76-82`, `.github/workflows/ci.yml:23-26`, `scripts/dev/setup_petta_env.sh:4-8`). Change them in all places together.

| Tool | Version | Why |
|---|---|---|
| Python | **3.12** | The hive and its tests. janus must be built against the same interpreter |
| SWI-Prolog | **10.1.14** (`swipl-devel`), **built against that Python 3.12** | PeTTa needs a working `library(janus)` Prolog-to-Python bridge |
| PeTTa | commit **`ae66fa8`** (`github.com/trueagi-io/PeTTa`) | The MeTTa runtime for minds and the shared spaces |
| janus-swi | **1.5.3** | The Python-to-Prolog bridge |
| Node.js | **22.12 or later** (or 24) | UI build and tests; vitest 5 and vite 8 need it |

**The trap on macOS.** Homebrew's SWI-Prolog 10.0.2 loads, but its bridge fails with `janus:py_call/4` not found, and then every hive test errors with "PeTTa failed to start" (`README.md:84-89`). Build 10.1.14 into a private prefix with `scripts/dev/setup_petta_env.sh`, and put its `bin` first on `PATH`.

**Check the bridge first.** It must print `42` (`README.md:94`):

```bash
swipl -g 'use_module(library(janus)), py_call(operator:add(20,22),V), print(V), nl, halt'
```

**One-time setup.**

```bash
python3.12 -m venv .venv && . .venv/bin/activate
pip install -r hive/requirements.txt          # add -r requirements.txt for OmegaClaw minds
pip install janus-swi==1.5.3
bash scripts/dev/setup_petta_env.sh            # builds SWI-Prolog 10.1.14 and checks out PeTTa ae66fa8
export PETTA_PATH=~/PeTTa PATH=$HOME/swipl-patched/bin:$PATH
```

The script's options are `--prefix`, `--petta`, `--python` and `--runtime` (`scripts/dev/setup_petta_env.sh:15-18`). Its build prerequisites for macOS and Debian or Ubuntu are listed at `setup_petta_env.sh:23-26`.

## Before a heavy run

- **Check the load.** Run one heavy suite at a time. On a busy machine a few UI tests hit their 5-second timeout (`STATUS.md:78`).
- **Use a git checkout at the exact commit.** Code tests need a real repository, so a `git archive` copy fails them (`deploy/RUNBOOK.md` §7).
- **Do not edit the tree during a run.**
- **Never point a test at real data.** The MeTTa smoke runner skips files that may touch live memory unless you pass `--allow-live-memory` (`tests/run_metta_smokes.py:1-8`). Do not pass it.

## omegahive

| Suite | Command (from the repo root unless noted) | Last result | Time |
|---|---|---|---|
| Hive server | `python -m pytest -q -p no:cacheprovider hive/tests` | **2414 passed, 0 failed, 66 skipped** (`STATUS.md:15`) | about 8.5 to 11 minutes (`STATUS.md:15`, `README.md:120`) |
| Hive acceptance (real minds, mock model) | `HIVE_E2E=1 PETTA_PATH=~/PeTTa HIVE_CHROMADB_LIB=<path> python -m pytest -q hive/tests/test_acceptance.py hive/tests/test_phase2_acceptance.py hive/tests/test_sharing_acceptance.py` (`hive/tests/test_acceptance.py:5-8`) | no separate recorded count; skipped in the default run | about a minute for the first file (`test_acceptance.py:5`) |
| OmegaClaw core | `python -m unittest discover -q -s tests` | **374 run OK, 31 skipped** (`STATUS.md:16`) | short; PeTTa-free |
| MeTTa smokes | `python tests/run_metta_smokes.py` (needs the `--runtime` run script that `setup_petta_env.sh` writes) | no recorded count | |
| UI types | `cd hive/ui && npx tsc -b --noEmit` | **clean** (`STATUS.md:17`) | |
| UI lint | `cd hive/ui && npm run lint` | no recorded result in `STATUS.md`; CI runs it (`ci.yml`, job `hive-ui`) | |
| UI tests | `cd hive/ui && npx vitest run` | **3822 passed, 5 timed out, 39 skipped** (`STATUS.md:18`). The 5 were 5-second timeouts under load and pass when their file runs alone | |
| UI build | `cd hive/ui && npm ci && npm run build` | builds in CI (`ci.yml`, job `hive-ui`) | |
| Linux isolation check | `python -m pytest -q --basetemp=/tmp/ohsbx hive/tests/test_mind_sandbox_linux.py` as the service account (`deploy/RUNBOOK.md` §5). The short `--basetemp` keeps socket paths under 108 bytes | passed on the target server and in a Linux container at an earlier release (release report) | |
| Autotests (legacy) | `python -m pytest Autotests/mock` with the mock model and chat servers; the live files need a running legacy agent | no recorded count; outdated (`Autotests/LEGACY.md:3`) | |

**With the three port pull requests applied** (`omegahive` `STATUS.md`, "With the port pull requests applied"; measured 2026-10-11 on the pull-request branches rebased on `main` c8a9aed, on a heavily loaded shared machine):

| Suite | Branch | Result |
|---|---|---|
| Hive server, full | `port/idle-minds` | **2431 passed, 0 failed, 66 skipped** |
| OmegaClaw core | `port/idle-minds` | **384 run, 23 skipped, 2 failed**. The 2 are `test_channel_hive` daemon-restart tests that fail the same way on `main` on that machine; CI passes them. `tests/test_wait_quiet_runtime.py`: 6 of 6 with a booted runtime |
| UI types, lint, build | `port/demo-mode-fix`, `port/surface-followups-r4` | `tsc -b` clean; lint 0 errors; build OK |
| UI tests, full | `port/demo-mode-fix` (contains idle minds) | **3885 tests: 3824 passed, 22 timed out under load, 39 skipped**; each timed-out file passes when run alone |
| UI tests, targeted | `port/surface-followups-r4` | **682 tests: 677 passed, 5 timed out under load**; those files pass when run alone |

**What the 66 hive skips are.** Skips name their reason. The reasons in the source are: no PeTTa, no Node, Linux without Landlock or user namespaces, macOS without sandbox-exec, no Docker daemon or image, `HIVE_E2E` not set, and a missing sibling app repo such as `omegafusion` (`STATUS.md:20-23`; skip reasons in `hive/tests/*.py`). Without a working PeTTa most hive tests **error** rather than skip (`README.md:125`).

**Expected failure on a server.** `test_every_relayed_route_exists_in_the_intended_service_release` fails until the Code service release is installed beside the hive (`deploy/RUNBOOK.md` §7).

**Where the counts were measured.** `STATUS.md` says "this tree, from a clean clone, with the toolchain in the README" (`STATUS.md:9-11`). It does not name the operating system. The last recorded full Linux run was at an earlier release: 1009 passed, 27 skipped, 1 expected failure on the target server (release report, "Linux test suite").

## App repositories

Every app count below was measured on 2026-10-10 in a fresh Python 3.12.13 venv on macOS arm64, against an omegahive prep checkout (commit `7b1ce3f` or `e4571e9`), not against `34b0fb3`. Re-run against the release commit before relying on them.

| Repo | Tier | Command (from that repo's root) | Last result |
|---|---|---|---|
| omega-tools | Open | `python -m pytest -q tests` (with `requirements-dev.txt`) | **8 passed**; contract **COMPATIBLE** (80 items); concurrency recipes on real PeTTa **44 of 45** (one expected pin failure) |
| omegalibrary | Open | `python -m pytest -q tests` (omegalibrary `README.md:42`, `:57`) | **38 passed** with the hive's requirements, omegahive beside it and PeTTa; **37 passed, 1 skipped** with dev requirements only. Network is cut for every test |
| omegaplanner | Open | `PYTHONPATH=omegahive:. python -m pytest -q omegaplanner/tests` from the parent folder, with the hive's requirements (omegaplanner `README.md:61`) | **84 passed, 11 skipped** with PeTTa; **76 passed, 11 skipped** without |
| omegahive-candidates | Open | `PYTHONPATH=.:<omegahive>:$PETTA_PATH/python python -m pytest -q <folder>/tests`, per folder | **483 passed, 22 skipped, 0 failed** in total across 10 folders |
| omegacode | Closed | `python -m pytest -q` | **642 passed, 107 skipped, 0 failed**. The owner-layout run (`-m owner_workspace`, 62 passed) needs toolchains that are not published |
| omegadesign | Closed | `node --test 'tests/**/*.test.mjs'` | **76 passed** (Node 26.0.0 and 24.19.0). The contract check needs a hive with the async-`view()` checker fix |
| omegafusion | Closed | `PYTHONPATH=<omegahive>:. python -m pytest tests qualification integration_r17 -q` | **97 passed, 1 skipped** with PeTTa; 58 passed, 40 skipped without |
| omegapurple | Closed | `python -m pytest -q omegapurple/tests omegapurple/security/tests` from the parent folder, with omegahive-candidates on `PYTHONPATH` | **233 passed, 2 skipped** |
| omegasocial | Closed | `python -m pytest -q tests qualification` | **43 passed, 12 skipped** |
| omegaatlas | Closed (private app) | `pytest backend/tests`; `pytest tests/integration` | **99 passed, 1 skipped**; **134 passed**. The frontend smoke was **not run** (no Chromium) |
| omegatruth | Closed (private app) | `pytest tests` | **181 passed** |
| omegav2 | Closed | `python -m pytest -q -p no:cacheprovider <file>`, each of 70 files on its own | 478 collected: **184 passed, 212 failed, 78 errors, 4 skipped**. 192 of the 290 failures and errors are `runtime-bundle-absent` |

**Contract check for any app.** `python -m hive.programs_check <app folder>` from an omegahive checkout. A COMPATIBLE result is a shape check, not proof that the app loads in a hive (see [connect a new app](../06-apps/03-connect-a-new-app.md), "Known gap").

## CI

`.github/workflows/ci.yml` defines three blocking jobs on `ubuntu-24.04`: `core-tests`, `hive-petta` (builds the pinned toolchain, caches it by pin, runs `hive/tests` with `-rs`) and `hive-ui` (Node 22, `npm ci`, typecheck, lint, vitest, build). It runs on every push and pull request and **passes on GitHub Actions** (omegahive PR #3). The first run passed `core-tests` and `hive-ui`, and 2402 hive tests; its 19 failures were the Linux mind-sandbox tests, which need unprivileged user namespaces (now enabled in the job, `ci.yml:66-69`), and one test that assumed SQLite's `secure_delete` default (`ci.yml:12-15`). It does not run the MeTTa smokes, the opt-in acceptance files, the Autotests or any app repo.

## References

- `README.md:72-133`
- `STATUS.md:9-22`, `:78`
- `.github/workflows/ci.yml:1-94`
- `scripts/dev/setup_petta_env.sh:1-26`
- `deploy/RUNBOOK.md` §5, §7
- `hive/tests/test_acceptance.py:1-22`
- `tests/run_metta_smokes.py:1-8`
- `docs/handoff/platform/release-report-2026-10-06.md` ("Linux test suite")
- `STATUS.md` in omega-tools, omegalibrary, omegaplanner, omegahive-candidates, omegacode, omegadesign, omegafusion, omegapurple, omegasocial, omegaatlas, omegatruth, omegav2
