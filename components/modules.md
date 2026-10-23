# Modules
> Seam-register card. Code refs are to `omegahive` @ 34b0fb3 unless another repo is named. Back to the [register](README.md).

## What it does
A module adds a skill, sense, channel, memory organ or body app to a mind without editing the core. Each module is a folder under `modules/` with a metadata manifest and MeTTa files that declare what it provides. The mind loads every module listed in one loader file at boot, and the command parser reads the same list, so a module is callable only when it is imported. On a hive, every module skill also passes the hive's policy gate.

Upstream: [OmegaClaw Core](https://github.com/PhysixSNET/omegahive-start-here/blob/main/ACKNOWLEDGEMENTS.md#omegaclaw-core).

## Where it lives
- Folders: `modules/<name>/` with `module.toml`, `entry.metta`, `catalog.metta`, `signatures.metta`, optional `affordance.metta`, `skills.metta` and `src/` (`docs/reference-omegaclaw-module-contract.md:13-24`).
- Loader: `modules/loader.metta:4-21`, one `import!` per enabled module; load order matters (`modules/loader.metta:7-9`).
- Composition: `lib_omegaclaw.metta:8-11` imports the loader after the core substrate and before the loop.
- Parser: `src/helper_command_parser.py:105-157` reads enabled names from the loader and each module's signatures and catalog.
- Gate: `hive/core/policy.py:23-58` (reviewed hive skills and defaults), `hive/core/policy.py:213-219` (the default decision).
- Per-mind link to the shared core: `hive/supervisor/workspace.py:181`.

## Contract at its edge
- **Manifest:** `module.toml` keys `id`, `kind`, `version`, `entrypoint`, `catalog`, `signatures`, `optional`, `default_enabled`, `provides` (`kind:name`), `requires`, `[env]`, `[trace]` (`modules/web_search/module.toml:1-28`).
- **Cognitive contract:** `entry.metta` mirrors the manifest as atoms such as `(Module id)`, `(ModuleKind id kind)`, `(Provides id (Skill name))`, `(TraceWrites id Event)` (`modules/web_search/entry.metta:4-32`).
- **Skill surface:** `(SkillSignature name (Arg type slot))` in `signatures.metta`; `SkillCatalog` and `SkillHelp` in `catalog.metta`; `Risk` and `Effect` in `affordance.metta` (`modules/scratch_space/signatures.metta:5-15`, `modules/scratch_space/affordance.metta:1-26`).
- **Hooks and spaces:** `(RuntimeOrgan name call)` and `(RuntimeHook response name call)`, each with a matching trusted atom; `register-space` for a module that owns a space (`modules/scratch_space/entry.metta:19-24`, `modules/scratch_space/skills.metta:3-9`).
- **Hive limits:** only allowlisted variables reach a hive mind, so `[env]` secrets do not (`hive/supervisor/sandbox.py:22-36`). Unknown skills are allowed by default; `hive-*` skills ask until reviewed (`hive/core/policy.py:23-28`, `:219`).
- **Scope today:** hive-wide. Every mind links the same core checkout, so one loader serves all minds on a hive (`hive/supervisor/workspace.py:181`, `lib_omegaclaw.metta:9`).

## Status and known issues
**Built**, hive-wide only. See `STATUS.md:76`: many modules are not yet ported to this hive and their compatibility is untested. The `modules/` folder carries a legacy note (`modules/LEGACY.md:1-3`), and at 34b0fb3 the contract doc does too (`docs/reference-omegaclaw-module-contract.md:1`); the contract itself is what shipped modules and tests enforce. Open findings in FINDINGS.md (in the private omegahive-security repo; ask Kabir): K27 (default web search and vision modules open their own connections), K28 (`[env]` secrets never reach hive minds), K30 (unknown skills default to allow), K33 and K55 (contract doc marker and sample), K52 (no per-mind scope).

**Intended: a scope per module.** The owner's design (2026-10-10) is that each module declares where it applies: **per mind**, **hive-wide**, **both**, or **neither** (installed, enabled for nobody until chosen). The right scope depends on the module and the use case: a sense or body app may belong to one mind, a shared channel or tool may serve the whole hive, and a skill may be offered hive-wide and switched on per mind. The intended shape adds a scope field to `module.toml` and a per-mind enable list read at mind start; a mind's list only narrows what the hive allows. Not designed in detail yet; see [03-modules.md](../03-minds/03-modules.md#intended-shape-and-upgrade-path).

## Tests that guard it
`tests/test_module_contract.py` (contract shape, fixtures under `tests/fixtures/modules/`), `tests/test_module_organs.py:157-193` (manifest and atoms agree), `tests/test_syntax_module_smoke.py`, the per-module `tests/module_*_smoke.metta` files, and `hive/tests/test_policy_hive_skills.py` (every `hive-*` skill is reviewed). No test checks scope, because scope does not exist yet.

## Swap point
**Yes**, per module. A replacement module must keep the manifest keys, mirror them as atoms in `entry.metta`, declare a signature and catalog line for each skill, and pass `tests/test_module_contract.py` and `tests/test_module_organs.py`. A team organ (for example a reasoning or attention organ) enters the same way, through the module contract and its hooks (`docs/EARLIER_EXPERIMENTS.md:26`, `:42`, `:45`). Swapping the module system itself means swapping the [mind runtime](mind-runtime.md).

## Equivalent in the SingularityNET stack
Options to evaluate: Hyperon's own module and package mechanism for MeTTa (`import!` of named libraries is already the load path), and the separate Omega V2 body's organ registry (closed tier, `omegav2`), whose organs would each enter here as a module.

## Keep criteria
Keep if every default module passes the contract tests from a clean clone, every side-effecting skill has an ask rule or a written ruling (K30), modules that open their own connections run only under the OS sandbox (K27), and the per-module scope is designed before any module that should belong to one mind ships to a shared hive.

## Read next
[03-minds/03-modules](../03-minds/03-modules.md), [mind-runtime](mind-runtime.md), [policy-and-approvals](policy-and-approvals.md), [07-upgrade-path/02-swap-seams](../07-upgrade-path/02-swap-seams.md), [08-reviewers/03-review-checklists](../08-reviewers/03-review-checklists.md), [10-testing/01-test-map](../10-testing/01-test-map.md).
