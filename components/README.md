# Component cards and seam register

One row per component of OmegaHive. Each card says what the part does, where it lives (`path:line`), the contract at its edge, its status and tests, what a replacement must satisfy, and options from the SingularityNET stack to evaluate. Use it to decide, part by part, whether to keep a component or swap in your own module.

- **Code refs:** the `omegahive` repo at commit 34b0fb3, unless a card names another repo. Line numbers drift; search for the named symbol if a line has moved.
- **Status:** **built** = in the code and live or tested; **partial** = built in part, opt-in, held or unverified; **intended** = designed, not built. Card text says which parts are which, with the source.
- **Tier:** **open** = Apache-2.0 code in `omegahive`. **Seam to closed** = an open seam whose other side is a closed-tier repo or folder; those internals are described in that repo's own `docs/schematics/`, not here.
- **Swap point:** **yes** = there is a defined edge a replacement can meet today; **no** = the part is cross-cutting or part of the core model, so a swap first needs a new seam.
- **Owners:** every card starts unassigned; the ownership and evidence matrix (in the private omegahive-security repo; ask Kabir) lists each card's dependencies, sign-off role and evidence location.
- **Known issues:** each card links `STATUS.md` in `omegahive`. K-numbers (K1 to K66) are the code and doc findings in 07-upgrade-path/FINDINGS.md (in the private omegahive-security repo; ask Kabir), grouped by severity on 03-hardening-for-launch.md (in the private omegahive-security repo; ask Kabir).

## Register

| Component | What it does | Tier | Status | Contract at its edge | Swap point | Card |
|---|---|---|---|---|---|---|
| People and auth | Password and invite-only Google sign-in, roles, public gate | Open | built | `/api/auth/*`, session with principal and role; public requests never reach mind routes | yes | [people-and-auth](people-and-auth.md) |
| Visibility | Private, shared, public; filters lists, reads and live events | Open | built | `hive.visibility` on every route; `EVENT_RULES` per event kind | no | [visibility](visibility.md) |
| Ask and conductor | Ask on every page; routing; optional host model loop that steers the screen | Open | built (conductor off by default) | `/api/ask*` frames; action vocabulary v1; per-turn limits | yes (conductor) | [ask-and-conductor](ask-and-conductor.md) |
| Swarms and rooms | Groups of minds and people; rooms, team rooms, sessions, roles | Open | built | `/api/swarms*`, `/api/rooms*`, `/api/agent/rooms*` | no | [swarms-and-rooms](swarms-and-rooms.md) |
| Goals and motivations | Tasks with leases and reviews; motivations above them; wakeups | Open | built | `/api/agent/goals*` claim, heartbeat, result; `/api/motivations`, `/api/tasks` | yes | [goals-and-motivations](goals-and-motivations.md) |
| Flows | Typed flow graphs turned into goal runs | Open | built | `omegaflow/1` IR; `/api/flows*`, `/api/agent/flows*` | yes | [flows](flows.md) |
| Between swarms | Connection agreements, cross-swarm requests, artifacts, findings | Open | built | `/api/connections*`, `/api/agent/requests*`, `/api/agent/artifacts*` | no | [between-swarms](between-swarms.md) |
| Agent hub | A native mind's WebSocket plus `/api/agent/*` REST | Open | built | `/agent-hub` frames `resume`, `agent_message`, `prompt_ack`; bearer member token | yes | [agent-hub](agent-hub.md) |
| MCP interface | Outside agents join a swarm as members | Open | built | `POST /mcp`, schema `s3-r1`, fixed `hive_*` tools | yes | [mcp-interface](mcp-interface.md) |
| LLM gateway and providers | The path for the hive's configured model and embedding calls; keys, metering, local-only rule (module egress is outside it, K27) | Open | built | OpenAI-compatible `/llm/v1/chat/completions`, `/embeddings`; `provider/model` | yes | [llm-gateway-and-providers](llm-gateway-and-providers.md) |
| Budgets | Limits at every level, worst-case check, durable reservations | Open | built | rule `(scope, period, limit_usd)`; 402 `spend_limit`; reserve, dispatch, settle | yes | [budgets](budgets.md) |
| Assets and media | Content-addressed files; metered image route | Open | partial | `/api/assets*`; store `put/get/has/delete`; `/llm/v1/media` (off) | yes (store) | [assets-and-media](assets-and-media.md) |
| Policy and approvals | Allow, ask or deny before a skill (bypasses: local skip list, unknown-skill allow; K10, K30); five-way approvals | Open | built | `POST /api/agent/authorize`; rules and `/api/approvals*` | yes | [policy-and-approvals](policy-and-approvals.md) |
| Capability tokens and delegation | HMAC tokens for services; leases for coordinators | Open | built | `hc1.<claims>.<sig>` plus live status; `/api/lifecycle/*` leases | yes | [capability-tokens-and-delegation](capability-tokens-and-delegation.md) |
| Supervisor and drivers | Keeps mind processes in their desired state | Open | partial (Docker unverified) | `Driver` interface `start/stop/status/logs/execution`; mind environment | yes | [supervisor-and-drivers](supervisor-and-drivers.md) |
| OS sandbox | Landlock and namespaces on Linux, sandbox-exec on macOS | Open | partial (opt-in) | `HIVE_MIND_SANDBOX=1`; `wrap(...)`; fail closed | yes | [sandbox](sandbox.md) |
| Power | Off, Wake all, Stop all with a durable snapshot | Open | built | `/api/hive/power`, `/api/hive/stop-all` | no | [power](power.md) |
| Child minds | A controller runs child minds for one request | Open | partial (held) | `HIVE_MIND_SPAWN`; `/api/agent/minds*` | no | [child-minds](child-minds.md) |
| Mind runtime (OmegaClaw) | The program each native mind runs, on PeTTa | Open | built | hub frames, `/api/agent/*`, gateway, `authorize`; `module.toml` | yes | [mind-runtime](mind-runtime.md) |
| Modules | Skills, senses, channels and organs added to a mind through one loader | Open | built (hive-wide; per-module scope intended) | `module.toml` plus `entry.metta` atoms; `modules/loader.metta`; policy gate per skill | yes (per module) | [modules](modules.md) |
| Mind memory | A mind's own AtomSpace spaces plus ChromaDB recall | Open | built (weak default embedder) | `memory/*.metta`; `remember`; `/api/agents/{id}/memory*` | yes | [mind-memory](mind-memory.md) |
| Mind observability | Traces, health, the idle monitor (Health asks an idle mind one question), tool inventory, archive | Open | built | `/api/agent/trace`, `/api/agent/inventory`; `hive_capabilities`; `/api/health/idle`, `/api/agents/{id}/health/idle`, `.../health/remind` | yes (export) | [mind-observability](mind-observability.md) |
| Channels | How a mind talks outward; hive channel for hive minds | Open, one closed folder | partial | `module.toml` `kind = "channel"`; adapter functions; `CHANNEL_EVENT` | yes | [channels](channels.md) |
| Hive spaces and commons | Per-swarm MeTTa commons in embedded PeTTa (`lib_hive`); read-only repository-map spaces | Open | built (K1, K3 to K5 open) | `/api/agent/publish`, `/query`, `/belief`; `(stv f c)`; outcome set; `/api/repo-maps*` | yes | [hive-spaces](hive-spaces.md) |
| Reasoning libraries | NAL, PLN, NARS as skills in every mind | Open | partial (not wired to the loop) | `nal-step`, `pln-step`, `nars-query`, `nars-derive`; `(stv f c)` | yes | [reasoning](reasoning.md) |
| Programs host and contract | Loads apps; work graphs; actions | Seam to closed | built (v0.1) | `describe/view/act`; `/api/programs*`; `python -m hive.programs_check` | yes | [programs-host](programs-host.md) |
| App pins | Load only the reviewed release of each app | Open | built | `HIVE_APP_PINS`, `HIVE_APP_PINS_REQUIRED`; refusal reasons | yes | [app-pins](app-pins.md) |
| App frame | An app's own UI in a sandboxed iframe | Seam to closed | built | `postMessage` ops on a per-frame channel; rate limits; lock and pin | yes (apps) | [app-frame](app-frame.md) |
| Native Tools | Reviewed tools for minds, off by default | Seam to open repo | built | `options.tools`; `GET /api/tools` | yes | [native-tools](native-tools.md) |
| Lab and Evolve | Benchmarks from the UI; Evolve host-side records | Seam to closed | partial | `/api/lab/*`; `ProgramContext.evolve_*` | yes (runner) | [lab-and-evolve](lab-and-evolve.md) |
| Code proxy | Relays an allow-list of Code service routes | Seam to closed | partial (cloud in review) | `/api/code/proxy/{path}`; `hc1` capability; release check | yes | [code-proxy](code-proxy.md) |
| UI shell and experiences | Web UI, looks, whole alternative front ends | Open, one closed folder | partial | `ExperienceDef` in the registry; `UiVariant`; REST and events | yes | [ui-shell](ui-shell.md) |
| SQLite state | Control-plane store; one process per data folder | Open | built | `HIVE_DATA_DIR`; `hive.db` (WAL); `Database` API | no | [sqlite-state](sqlite-state.md) |
| Events and live updates | Fans typed events out to browsers, filtered per viewer | Open | built | `/api/events` socket; `{type, at, ...}`; `EVENT_RULES` | yes | [events](events.md) |
| Federation | Moving a mind between hives today; hive-to-hive intended | Open | intended (move partial) | export, import, settle routes; intended signed belief bundles | yes (open design) | [federation](federation.md) |

## Where the diagrams are
Schematics sections: [01-system](../01-system/), [02-ask-and-ui](../02-ask-and-ui/), [03-minds](../03-minds/), [04-knowledge](../04-knowledge/), [05-governance](../05-governance/), [06-apps](../06-apps/), [07-upgrade-path](../07-upgrade-path/), [08-reviewers](../08-reviewers/), 09-security-and-launch (in the private omegahive-security repo; ask Kabir), [10-testing](../10-testing/). Read [`LEGEND.md`](../LEGEND.md) first.
