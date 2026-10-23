# Federation (intended)
> Seam-register card. Code refs are to `omegahive` @ 34b0fb3 unless another repo is named. Back to the [register](README.md).

## What it does
Today: a mind can be moved between hives (export, import, settle), and a person's representative can talk to the cloud hive. Intended: each person's hive is a node that talks to other hives, sharing stamped beliefs in the style of DAS shards. Hive-to-hive linking is not built.

Upstream: [MORK and DAS](https://github.com/PhysixSNET/omegahive-start-here/blob/main/ACKNOWLEDGEMENTS.md#mork-and-das), [ASI:Chain](https://github.com/PhysixSNET/omegahive-start-here/blob/main/ACKNOWLEDGEMENTS.md#asi-chain).

## Where it lives
- Built, the move: `hive/core/placement.py:1-14` (export, import, settle; placement evidence), `:56` `Placement`: `export` `:110`, `import_` `:205`, `settle` `:342`; routes `hive/core/app.py:1861-1906`.
- Built, inside one swarm only: shares and exhibits, which "never cross swarms" (`hive/core/shares.py:3-14`).
- Unused hook: `hive-view` union over several spaces (`hive/spaces/lib_hive.metta:145-152`); `Hive.query` passes only the mind's own swarm (`hive/core/hive.py:1642`).
- Intent: `docs/theory/ledger-provenance-and-das.md:84-134` (design and the six-step road); `docs/FEATURES.md:143` (SW23).

## Contract at its edge
- **Move:** `POST /api/agents/{id}/export` (a bundle with `manifest.json` and `workspace/`, hashes for every file; a personal mind's bundle carries its person's chats only for that person or an explicit audit and imports only back home, 409 `personal_mind_unbound`; rows that would change owner are refused, 409 `conversation_owner_mismatch`, with the omegahive pull request `port/idle-minds-r2.5`), `POST /api/agents/import`, `POST /api/agents/{id}/settle`, `GET /api/agents/{id}/moves`; hive identity `GET|PATCH /api/hive/identity`.
- **Intended:** a per-hive ed25519 key; signed bundles of stamped beliefs; peers mounted as remote spaces with a local cache; a hash-chained spaces log; trust discount on incoming confidence. None of these exist yet.

## Status and known issues
**Intended**, with one partial piece. Hive-to-hive is not complete (`STATUS.md:71`); FEATURES says no reviewed plan was found (`docs/FEATURES.md:143`). The move code is deployed but no live move has succeeded (`docs/FEATURES.md:101`). **K1:** FEATURES CR3 says belief queries reach "the federation", but the code searches only the mind's swarm (`hive/core/hive.py:1642`).

## Tests that guard it
`hive/tests/test_placement.py`, `test_shares_api.py`, `test_share_visibility.py`, `test_sharing_acceptance.py`. Nothing tests hive-to-hive, because it is not built.

## Swap point
**Yes**, and open: this is the natural place for the team's own distributed stack. A design must keep evidence stamps across hives (so revision stays honest), single-writer ownership of each swarm commons, and the visibility rules. Conformance test: none yet, write one first.

## Equivalent in the SingularityNET stack
Options to evaluate: DAS `RemoteAtomDB` for mounting a peer's commons and DAS `AuthorizationManifest` for per-pattern access; MORK as a storage backend; ASI:Chain later for anchoring signed chain heads, never for authorisation (`docs/theory/ledger-provenance-and-das.md:84-91,108-111`).

## Keep criteria
There is nothing to keep yet beyond the move. Keep the move if a live round trip (export, import, settle, move back) succeeds with hashes checked and the tombstone respected.

## Read next
[04-knowledge/04-federation](../04-knowledge/04-federation.md), [04-knowledge/02-beliefs-sharing](../04-knowledge/02-beliefs-sharing.md), [05-governance/05-intended-governance](../05-governance/05-intended-governance.md), [07-upgrade-path/02-swap-seams, federation](../07-upgrade-path/02-swap-seams.md#11-federation), [07-upgrade-path/01-intended-evolution](../07-upgrade-path/01-intended-evolution.md), 09-security-and-launch/01-threat-model, TB9 (in the private omegahive-security repo; ask Kabir), [08-reviewers/02-invariants, I-F](../08-reviewers/02-invariants.md#i-f-federation-and-moves).
