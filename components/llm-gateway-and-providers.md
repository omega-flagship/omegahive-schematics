# LLM gateway and providers
> Seam-register card. Code refs are to `omegahive` @ 34b0fb3 unless another repo is named. Back to the [register](README.md).

## What it does
The path for the hive's configured model and embedding calls. It is not an egress boundary: a module skill can open its own network connection, which the gateway never sees and only the OS sandbox (opt-in today) stops (K27; [sandbox](sandbox.md); launch items ISO3 and PRI5 in the checklist (in the private omegahive-security repo; ask Kabir)). Minds call an OpenAI-compatible endpoint with their own hive token. The gateway picks the provider from the mind's `provider/model`, injects the key, meters tokens and cost, enforces budgets and the local-only rule for those calls, and never hands keys to minds. `mock/echo` lets a hive run with no provider.

Upstream: [LLM organ](https://github.com/PhysixSNET/omegahive-start-here/blob/main/ACKNOWLEDGEMENTS.md#llm-organ).

## Where it lives
- `hive/core/gateway.py:1-9` (contract), `:224` `Gateway`: `enforce_egress` `:230`, `paying_key` `:265`, `estimate` `:286`, `cost` `:336`, `chat` `:340`, `embeddings` `:376`; offline models `mock_reply` `:87`, `mock_embedding` `:213`.
- `hive/core/providers.py:85` `ProviderStore`: keys, catalogue, per-model routing (`openrouter_routing` `:434`).
- Routes: `POST /llm/v1/chat/completions` `hive/core/app.py:2063`, `POST /llm/v1/embeddings` `:2145`, models and providers `:1003-1138`, keys `:1084-1120`.
- Media route (off by default): `hive/core/media.py:1`, `app.py:2134`.

## Contract at its edge
- **Request:** OpenAI chat-completions body. The host sets `max_tokens` to 4096 when absent so the reservation is a true worst case (`app.py:2067-2068`).
- **Model id:** `<provider>/<model>` (`gateway.py:58` `split_model`).
- **Settings:** `HIVE_LOCAL_ONLY_SWARMS` (`gateway.py:232`), `HIVE_ALLOW_UNPRICED` (`gateway.py:302`; fails closed today, see K12 in FINDINGS.md (in the private omegahive-security repo; ask Kabir)), provider key variables named per provider, `HIVE_MEDIA_ROUTE`.
- **Errors:** `GatewayError` with status and code, for example 403 `egress_refused`.

## Status and known issues
**Built.** `STATUS.md:35-38`. Local-only swarms were verified live (`STATUS.md:38`). The skill policy gate is a separate engine (see [policy and approvals](policy-and-approvals.md)).

## Tests that guard it
`hive/tests/test_local_only_egress.py`, `test_providers_api.py`, `test_sso_and_budgets.py`, `test_cost_reservations.py`, `test_media_route.py`; runtime side `tests/test_llm_provider.py`.

## Swap point
**Yes.** A provider plugs in behind `ProviderStore`; a whole replacement gateway must keep the OpenAI-compatible routes, reserve worst-case cost before dispatch, settle actual cost after, and refuse egress for local-only swarms. Conformance test: none yet, write one first.

## Equivalent in the SingularityNET stack
Options to evaluate: SingularityNET platform AI services, reached through the marketplace daemon and its payment channels, as one more provider; a self-hosted model as a local-only provider.

## Keep criteria
Keep if every paid call path goes through `estimate`, reservation and settle (no direct provider calls elsewhere), and local-only refusal is tested for every provider.

## Read next
[05-governance/02-budgets-and-spend](../05-governance/02-budgets-and-spend.md), [03-minds/03-modules](../03-minds/03-modules.md), [01-system/04-request-lifecycle](../01-system/04-request-lifecycle.md), [03-minds/05-models-and-gateway](../03-minds/05-models-and-gateway.md), [07-upgrade-path/02-swap-seams, gateway](../07-upgrade-path/02-swap-seams.md#7-the-model-gateway), 09-security-and-launch/01-threat-model, TB6 (in the private omegahive-security repo; ask Kabir), [08-reviewers/02-invariants, I-G](../08-reviewers/02-invariants.md#i-g-spend-and-models), [08-reviewers/03-review-checklists, models](../08-reviewers/03-review-checklists.md#4-models-gateway-and-spend).
