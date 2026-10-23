# End-to-end scenarios to add first
> These are proposals. None of them exists as a default-run test today. Code refs are to omegahive @ 34b0fb3 unless named.

**What this shows.** The end-to-end scenarios that would close the largest [testing gaps](03-gaps.md) and the open launch risks (in the private omegahive-security repo; ask Kabir), in the order to build them, then the [capacity scenarios](#capacity-scenarios-workload-to-be-chosen) a launch also needs.

**Who should read it.** Whoever builds the test harness for the launch, and component owners whose card a scenario touches.

## Ground rules for every scenario

- **Disposable and synthetic.** A fresh data directory per run, invented people and minds, the offline `mock/echo` model or a loopback `local` provider. No real data, no real accounts.
- **Runs by default on the launch OS.** Linux in CI, plus macOS for the developer path. A scenario that only runs when opted in does not close G2.
- **Drives the real surfaces.** A browser for the UI (`playwright-core` is already a UI dev dependency, `hive/ui/package.json:52`, used by `hive/ui/src/lib/appFrame.browser.test.ts:12`), HTTP for the API, a real mind process for minds.
- **Asserts on observable outcomes,** not on internal calls: what the person sees, what the API answers, what is on disk.
- **The existing opt-in acceptance files are a starting point** (`hive/tests/test_acceptance.py`, `test_phase2_acceptance.py`, `test_sharing_acceptance.py`): they already start a real hive with real minds and a mock model.

## The first five

| Order | Scenario | Closes | Components |
|---|---|---|---|
| 1 | Fresh Linux install to a first conversation | G4, G6, G7; checklist OPS3, ISO4, TST4 | [supervisor](../components/supervisor-and-drivers.md), [sandbox](../components/sandbox.md), [mind-runtime](../components/mind-runtime.md), [ask-conductor](../components/ask-and-conductor.md) |
| 2 | Public boundary through a real proxy | R1, R5; checklist SEC2, SEC3 | [people-auth](../components/people-and-auth.md), [agent-hub](../components/agent-hub.md) |
| 3 | Sandbox escape probes from a real mind | R2, R10, R11; checklist ISO3 to ISO5 | [sandbox](../components/sandbox.md), [supervisor](../components/supervisor-and-drivers.md) |
| 4 | Approval round trip in the browser | G3, R7, R8; checklist GOV5, GOV6, TST6 | [policy-approvals](../components/policy-and-approvals.md), [ui-shell](../components/ui-shell.md), [mind-runtime](../components/mind-runtime.md) |
| 5 | Shared beliefs survive a crash and a restore | G2, G17, R14; checklist DAT3 to DAT5 | [hive-spaces](../components/hive-spaces.md), [sqlite-state](../components/sqlite-state.md) |

### 1. Fresh Linux install to a first conversation
- **Setup.** A clean Ubuntu host or VM. Follow `deploy/RUNBOOK.md` §0 to §7 exactly, including `deploy/setup_runtime.sh`, with `HIVE_MIND_SANDBOX=1`.
- **Steps.** Sign in as the first admin. Create a swarm. Create a native mind on the mock model and start it. In a browser, ask it something through the Ask.
- **Pass.** The mind's reply appears in the page. A `*.landlock.json` profile exists for the mind, and its log has no "mind isolation failed" (`deploy/RUNBOOK.md` §7). The full `hive/tests` run on the same host is green apart from the documented expected failure.

### 2. Public boundary through a real proxy
- **Setup.** The hive behind nginx and, separately, Caddy, each with the runbook's settings. Then a deliberately wrong proxy that strips the prefix and sets no forwarding header.
- **Steps.** From outside: call `/agent-hub`, `/llm/`, `/api/agent/*`, `/api/auth/login` with the password, a `/..` path, and an operator route with `?token=`.
- **Pass.** Agent routes 404, password login 403, traversal 400 (`hive/core/sso.py:121-126`). With the wrong proxy, the test **must fail** until R1 is fixed; it is the regression test for that fix.

### 3. Sandbox escape probes from a real mind
- **Setup.** One native mind with `HIVE_MIND_SANDBOX=1` on Linux (Landlock ABI 1 and ABI 4 or later, if both kernels are available) and on macOS.
- **Steps.** From the mind's shell skill: read the hive's data directory and settings file, list its environment, open a TCP connection to a port that is not allowed, create a unix socket, read another mind's folder, run a module that opens its own outbound connection, and allocate memory without bound.
- **Pass.** Every file, socket and network attempt is refused. No secret-looking variable is present (`hive/supervisor/sandbox.py:22-36`). The memory test records what happens today (no limit, R10) and becomes a pass once limits exist. Start from the bypass probes already in `hive/tests/test_mind_sandbox_linux.py`.

### 4. Approval round trip in the browser
- **Setup.** Two people, one admin and one member, each signed in in a browser. One native mind with an ask-mode skill.
- **Steps.** The mind tries the skill. The admin sees the approval and answers Once. The mind retries; it runs once; a second try asks again. Then answer Never. Then the member tries to change a hive-scope rule and to answer an approval for a mind they cannot see. Then the mind runs a skill on the local list (`modules/hive/src/hive_commons.py:931-936`) that a hive rule denies.
- **Pass.** Each answer behaves as on the [permissions page](../05-governance/01-permissions-and-policy.md). The member and local-list steps record today's behaviour (R7, R8) until each is ruled on.

### 5. Shared beliefs survive a crash and a restore
- **Setup.** Three native minds in one swarm, as in `test_acceptance.py::test_three_omegas_share_revise_and_survive_restart`.
- **Steps.** Publish and revise beliefs. Kill the hive with SIGKILL during a publish. Restart. Then back up the data directory by the runbook, restore it on a second clean host, and start.
- **Pass.** After the crash, the commons and the `assertions` table agree, or the disagreement is detected and reported. After the restore, every belief, stamp and policy rule is present.

## Next in line

| Scenario | What it proves | Closes | Components |
|---|---|---|---|
| App release, mount, act and tamper | Pin a release; a person opens the app in its frame and does a confirm-required action; change one file; the app closes with `release_mismatch` until a reload (`hive/PROGRAMS.md:214-218`) | R3, G3 | [app-pins](../components/app-pins.md), [programs-host](../components/programs-host.md), [app-frame](../components/app-frame.md) |
| Code change with an exact approval | Enrol the Code service; open a target; a mind proposes an edit; approve; the service redeems the exact binding once; revoke the grant mid-task; the next mutation is refused (`hive/core/services.py:12-13`) | R9 | [code-proxy](../components/code-proxy.md), [capability-tokens](../components/capability-tokens-and-delegation.md) |
| Budget exhaustion and local-only egress | A mind with a small cap on a priced loopback provider calls until it is refused; holds settle; a local-only swarm refuses an outside provider | G11 | [budgets](../components/budgets.md), [gateway](../components/llm-gateway-and-providers.md) |
| External MCP member | Invite code, join, publish, query; reuse of the code refused; the 121st call in a minute refused (`hive/core/mcp.py:305-313`) | R15 | [mcp](../components/mcp-interface.md), [hive-spaces](../components/hive-spaces.md) |
| Two people, two personal minds | Neither person nor an admin by default sees the other's personal content; held copies leave no trace on disk after collection | PRI2, PRI3 | [visibility](../components/visibility.md), [ask-conductor](../components/ask-and-conductor.md) |
| Stop all, Off and Wake all with live minds | Live minds stop; a late hub connection is refused; Wake all restores exactly the set that was awake | INC2 | [supervisor](../components/supervisor-and-drivers.md), [agent-hub](../components/agent-hub.md) |
| Every experience in a browser | Sign in, open the Ask, reach every feature, on desktop and phone widths, for each reviewed experience | G3 | [ui-shell](../components/ui-shell.md) |
| Frontier features on Linux | Computer use, browser use, draw on screen and vibe coding on the Linux target | G5 | [code-proxy](../components/code-proxy.md), [ui-shell](../components/ui-shell.md) |
| A mind moves between two hives | Export, import with the same id and hashes, move back to the tombstone (`hive/core/placement.py:4-9`) | federation not verified live | [federation](../components/federation.md) |

## Capacity scenarios (workload to be chosen)

None of these exists today. They need a launch workload chosen first. **Team size is not a workload:** the number of people who will use the hive does not say how many are signed in at once, how many minds are awake, or how often they act. Do not assume 200 concurrent users, or any other number, until the launch lead writes the workload down.

### Workload assumptions to choose

Fill every value before a capacity run, and record who chose it and why.

| Parameter | Value | Chosen by | Basis |
|---|---|---|---|
| Concurrent signed-in people | to be chosen | launch lead | expected peak, not team size |
| Ask turns per person per hour | to be chosen | launch lead | |
| Awake native minds | to be chosen | launch lead | each is its own process with no resource limit today (K26) |
| Swarms, and minds per swarm | to be chosen | launch lead | |
| Model calls per mind per minute | to be chosen | models owner | use `mock/echo` or a loopback `local` provider, so the run spends nothing |
| Belief publishes and queries per minute | to be chosen | knowledge owner | |
| Live event subscribers (open pages) | to be chosen | UI lead | |
| External MCP members | to be chosen | minds owner | the per-member rate limit is 120 calls a minute (`hive/core/mcp.py:305-313`) |
| Launch host | to be chosen | operations lead | CPU, memory, disk and OS of the real target |

### Acceptance criteria to choose

| Criterion | Target | Measured as |
|---|---|---|
| Latency | to be chosen, per surface | p50 and p95 for page API reads, Ask admission, first reply frame, belief publish, event delivery |
| Saturation behaviour | to be chosen | the load at which a latency target is first missed, and which resource ran out first |
| Refusal, not failure | required | over capacity, the hive answers with a clear refusal (for example `ask_busy`, a rate-limit refusal or a budget 402), not timeouts, 500s or lost writes |
| Recovery time | to be chosen | from a crash or restart under load until every latency target is met again |
| No data loss | required | after recovery the commons, the `assertions` table and the policy rules agree with what was acknowledged |

### Scenarios

| # | Scenario | Steps | Pass |
|---|---|---|---|
| C1 | Steady load | Run the chosen workload for at least an hour on the launch host | every latency target met; no error rate above the chosen ceiling |
| C2 | Ramp to saturation | Raise people, minds and calls step by step past the chosen workload until a target fails | the first failure is a clear refusal; the run records the resource that saturated first (CPU, memory, SQLite writes, event fan-out or mind processes) |
| C3 | Mind count | Add awake minds one at a time on the launch host | per-mind memory and CPU recorded; the maximum safe count written into the runbook (no per-mind limit exists today, K26) |
| C4 | Recovery under load | At the chosen workload, kill the hive with SIGKILL, then restart it | recovery within the chosen time; the awake set is restored; no acknowledged write lost (see scenario 5) |
| C5 | Soak | The chosen workload for a long run (duration to be chosen) | memory, open files and database size grow only as the data grows |

Known structural limits to watch in these runs: the hive is one process per data directory over SQLite (see [sqlite-state](../components/sqlite-state.md)); one Ask turn per thread at a time; and the reconcile loop runs every step in one try, so one failing step skips the rest of the tick (K20, `hive/core/app.py:181-201`).

## References

- `deploy/RUNBOOK.md` §0 to §8
- `hive/tests/test_acceptance.py`, `test_phase2_acceptance.py`, `test_sharing_acceptance.py`, `test_mind_sandbox_linux.py`
- `hive/ui/src/lib/appFrame.browser.test.ts:1-25`
- `hive/core/sso.py:121-126`; `hive/core/services.py:1-17`; `hive/core/mcp.py:289-313`; `hive/core/placement.py:4-9`
- `hive/core/app.py:181-201` (reconcile loop)
- `hive/supervisor/sandbox.py:22-36`; `modules/hive/src/hive_commons.py:930-962`
- `hive/PROGRAMS.md:214-218`
