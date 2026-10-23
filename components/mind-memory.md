# Mind memory (AtomSpace plus ChromaDB)
> Seam-register card. Code refs are to `omegahive` @ 34b0fb3 unless another repo is named. Back to the [register](README.md).

## What it does
Each mind keeps its own memory. Named AtomSpace spaces (persistent, agenda, beliefs, world, events, activity, cleanup) are saved as one `.metta` file each in the mind's workspace, with size limits that never drop protected atoms (identity, pins, goals, commitments). Long-term recall embeds text into ChromaDB beside the AtomSpace. A promotion score feeds the best memories back as hints.

Upstream: [memory (ChromaDB)](https://github.com/PhysixSNET/omegahive-start-here/blob/main/ACKNOWLEDGEMENTS.md#memory-chromadb).

## Where it lives
- Spaces: `lib_omegaclaw_core.metta:40-46` (`bind!` of each space); registry and limits `src/skills_runtime_spaces.metta:14-31`.
- Recall: `src/memory.metta:65-67` (`remember`), promoted hints `:69-80`; ChromaDB library loaded at `lib_omegaclaw_core.metta:37-38`.
- Promotion map: `src/helper_promotion.py` (`memory/promotions.db`).
- ChromaDB library source for a workspace: `hive/supervisor/workspace.py:73-82` (`HIVE_CHROMADB_LIB`).
- Hive view of a mind's spaces: `GET /api/agents/{id}/memory`, `/memory/{space}`, retire and reset (`hive/core/app.py:2590-2606`).

## Contract at its edge
- **Files:** `memory/*.metta`, `memory/evicted.metta` (every eviction recorded), `memory/history.metta`, `memory/promotions.db`.
- **Skills:** `remember`, `query`, `episodes`, `pin`, `space-*` (defaults in `hive/core/policy.py:50-53`).
- **Embeddings:** through the gateway's `/llm/v1/embeddings`; the hive default embedder is `mock/hash` (`STATUS.md:52`).
- **Sharing:** only through timed shares and exhibits ([federation](federation.md) covers why it never crosses swarms).

## Status and known issues
**Built**, with a weak default. Recall quality depends on setting a real embedding model (`STATUS.md:52`). The ChromaDB library is fetched with `git-import!` at start (`lib_omegaclaw_core.metta:37`). Attention is a heuristic classifier with ECAN-inspired names (`STATUS.md:51`).

## Tests that guard it
Runtime: `tests/test_memory_runtime.py`, `test_memory_safety.py`, `test_multi_instance_memory.py`, `test_memory_file.py`, `memory_safety_smoke.metta`, `space_registry_smoke.metta`. Hive: `hive/tests/test_phase2_api.py` (memory routes), `test_shares_api.py`.

## Swap point
**Yes**, the vector store and the space store, separately. A vector store must provide `remember`, query by text and query by ids. A space store must keep protected atoms and record every eviction. Conformance test: none yet, write one first.

## Equivalent in the SingularityNET stack
Options to evaluate: MORK or DAS as the space store; an AtomSpace-native similarity index instead of ChromaDB; ECAN for forgetting and recall priority in place of the current heuristic.

## Keep criteria
Keep if a launch embedding model is set and measured, eviction never touches protected atoms in a fill test, and memory files survive a crash mid-save.

## Read next
[04-knowledge/01-metta-and-atomspace](../04-knowledge/01-metta-and-atomspace.md), [03-minds/01-mind-runtime](../03-minds/01-mind-runtime.md), [04-knowledge/02-beliefs-sharing](../04-knowledge/02-beliefs-sharing.md), [07-upgrade-path/02-swap-seams, memory recall](../07-upgrade-path/02-swap-seams.md#4-memory-recall), [08-reviewers/02-invariants, I-P](../08-reviewers/02-invariants.md#i-p-personal-memory).
