# Assets and media
> Seam-register card. Code refs are to `omegahive` @ 34b0fb3 unless another repo is named. Back to the [register](README.md).

## What it does
Assets are content-addressed binary files (images, PDFs, decks, design originals), stored locally or in an S3-compatible store; every read and transfer is checked against the sha256. The media route lets a mind ask for one image through the host, metered like a model call.

## Where it lives
- `hive/core/assets.py:1-11`, `LocalStore` `:51`, `S3Store` `:80`, `Assets` `:133`; routes `hive/core/app.py:3061-3115`.
- `hive/core/media.py:1`, `MediaRoute` `:366`; route `POST /llm/v1/media` (`app.py:2134`).

## Contract at its edge
- **Routes:** `POST /api/assets`, `GET /api/assets/{sha}`, `POST /api/assets/{sha}/transfer`; minds `POST /api/agent/assets`, `GET /api/agent/assets/{sha}`.
- **Settings:** `HIVE_ASSET_STORES` (extra stores), `HIVE_MEDIA_ROUTE=on`.
- **Store interface:** `put`, `get`, `has`, `delete` by digest (`assets.py:62-76`).

## Status and known issues
**Partial.** Assets built, local store in use. Media route built and off by default.

## Tests that guard it
`hive/tests/test_assets.py`, `test_mind_assets.py`, `test_media_route.py`.

## Swap point
**Yes**, the store: implement `put`, `get`, `has`, `delete` by digest. Conformance test: none yet, write one first.

## Equivalent in the SingularityNET stack
No direct equivalent known to this author.

## Keep criteria
Keep if an S3 store is tested end to end before it is used, and digests are checked on every read.

## Read next
[01-system/03-state-and-storage](../01-system/03-state-and-storage.md), [05-governance/02-budgets-and-spend](../05-governance/02-budgets-and-spend.md), [03-minds/05-models-and-gateway](../03-minds/05-models-and-gateway.md), 09-security-and-launch/01-threat-model, at rest (in the private omegahive-security repo; ask Kabir), [10-testing/01-test-map](../10-testing/01-test-map.md#components-and-their-tests).
