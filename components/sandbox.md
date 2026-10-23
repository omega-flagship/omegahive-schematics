# OS sandbox
> Seam-register card. Code refs are to `omegahive` @ 34b0fb3 unless another repo is named. Back to the [register](README.md).

## What it does
Wraps each mind process, and each app tool run, in the host's own OS boundary. On Linux it uses new namespaces plus Landlock file and port rules and a seccomp filter on Unix sockets. On macOS it uses `sandbox-exec`. A mind can write only its own workspace, read named runtime roots, and reach only the hive's own loopback ports.

## Where it lives
- `hive/supervisor/sandbox.py:39` `backend()` (which boundary this host has), `:53` `wrap`, `:82` `loopback_ports`, `:100` `profile`, `:128` `runtime_roots`, `:27` `mind_environment`.
- `hive/supervisor/landlock.py:135` `available`, `:139` `profile`, `:166` `restrict_files`, `:232` `deny_unix_sockets`, `:392` `_enter_namespaces`.
- `hive/supervisor/limits.sh:1-7` (CPU-seconds and file-size limits; exits 78 if a limit cannot be set).
- Switch in the local driver: `hive/supervisor/drivers.py:184-187`. App tool runs: `hive/core/sandbox_run.py:1`.

## Contract at its edge
- **Setting:** `HIVE_MIND_SANDBOX=1` turns it on; a host with no backend then refuses to start minds (`drivers.py:187`). `HIVE_MIND_SANDBOX_PORTS` adds loopback ports (`sandbox.py:82-98`).
- **Interface:** `wrap(command, mind_dir, read_roots, profile_dir, agent_id, ports, programs)` returns the wrapped command and the profile path it enforces.
- **Isolation report:** `GET /api/agents/{id}/isolation` (`hive/core/app.py:1911`).

## Status and known issues
**Partial.** Built and used on deployments, but opt-in: development hives run without it (`STATUS.md:54`). Delegation and child minds refuse to run without it.

## Tests that guard it
`hive/tests/test_mind_sandbox.py`, `test_mind_sandbox_linux.py` (needs a Linux host), `test_sandbox_run.py`.

## Swap point
**Yes.** A replacement (for example gVisor, Firecracker or a container runtime) must give the same guarantees: write only the workspace, read only named roots, reach only allowed loopback ports, no Unix sockets, CPU and file-size limits, and refuse to start when it cannot. Conformance test: `test_mind_sandbox_linux.py` is the closest; a backend-neutral probe suite does not exist yet, write one first.

## Equivalent in the SingularityNET stack
No equivalent in the Hyperon stack; this is host security. Option to evaluate: whatever isolation the team's own agent hosting already certifies.

## Keep criteria
Keep if a red-team probe run on the launch Linux kernel shows every guarantee above, and deployments fail closed when the sandbox is missing.

## Read next
[03-minds/02-supervisor-drivers-sandbox](../03-minds/02-supervisor-drivers-sandbox.md), [05-governance/04-isolation](../05-governance/04-isolation.md), [07-upgrade-path/02-swap-seams, sandbox](../07-upgrade-path/02-swap-seams.md#9-the-sandbox-and-drivers), 09-security-and-launch/01-threat-model, TB4 (in the private omegahive-security repo; ask Kabir), [08-reviewers/02-invariants, I-I](../08-reviewers/02-invariants.md#i-i-isolation), [10-testing/04-e2e-scenarios, scenario 3](../10-testing/04-e2e-scenarios.md#3-sandbox-escape-probes-from-a-real-mind).
