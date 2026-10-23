# OmegaHive schematics

> **Not yet reviewed.** This is handover material from PhysixSNET, published as received on 2026-10-23 so the review can happen in the open. Links still point to the original PhysixSNET repositories, which are private. The review and the fixes are tracked in this repository's issues.
>
> The Closed apps' pages are now in each app's private `-app` repository, and the security material (threat model, launch checklist, findings and hardening backlog) is in the private `omegahive-security` repository. Ask Kabir for access.

Diagrams and schematics for the whole OmegaHive platform. They have four jobs:

1. **How it works.** Every part, drawn from the code with `path:line` references.
2. **How it is intended to grow.** Solid lines are built; dashed lines are the intended shape.
3. **How to plug in.** Each owner can see exactly where their piece connects and what they must keep stable.
4. **What to review.** Reviewers can see what each part must guarantee and which tests guard it.

New here? Read [`LEGEND.md`](LEGEND.md), then [`00-start/`](00-start/).

Where each upstream piece comes from, with licences and papers: [Lineage and acknowledgements](https://github.com/PhysixSNET/omegahive-start-here/blob/main/ACKNOWLEDGEMENTS.md).

## Contents
| Section | What it covers |
|---|---|
| [00-start](00-start/) | The one-page picture, and where to go next for your role |
| [01-system](01-system/) | Platform overview, hive server map, state and storage, request lifecycle |
| [02-ask-and-ui](02-ask-and-ui/) | The Ask and the conductor, experiences and looks, the app frame |
| [03-minds](03-minds/) | Mind runtime, supervisor and sandbox, modules, channels and external members, models and the gateway |
| [04-knowledge](04-knowledge/) | MeTTa and AtomSpace, sharing beliefs, reasoning, federation |
| [05-governance](05-governance/) | Permissions and policy, budgets, visibility and privacy, isolation, the intended deeper governance |
| [06-apps](06-apps/) | Programs contract, app lifecycle, connecting a new app, one page per app |
| [components](components/) | One card per component: contract, tests, known issues, swap point, keep criteria |
| [07-upgrade-path](07-upgrade-path/) | The intended evolution in order, the swap seams, and the hardening backlog |
| [08-reviewers](08-reviewers/) | How to review, the invariants, per-area checklists |
| 09-security-and-launch (in the private omegahive-security repo; ask Kabir) | Threat model, launch-readiness checklist, and the ownership and evidence matrix |
| [10-testing](10-testing/) | Test map, how to run every suite, and the gaps |

## Where to find each job
| Job | Pages |
|---|---|
| How it works | Every page, "How it works" section |
| Intended upgrade | Every page, "Intended shape" section, plus `07-upgrade-path/` |
| Keep or swap a component | `components/`, `07-upgrade-path/02-swap-seams.md`, and the rubric in `omegahive-start-here/onboarding/DECIDE.md` |
| Plug in your piece | `03-minds/03-modules.md`, `03-minds/05-models-and-gateway.md`, `06-apps/03-connect-a-new-app.md`, `06-apps/apps/*` |
| Review | Every page, "For reviewers" section, plus `08-reviewers/`, `09-security-and-launch/` and `10-testing/` |

The diagrams are mermaid, so they draw directly on GitHub. The code lives in the `omegahive` repo and the app repos. This repo only describes it.
