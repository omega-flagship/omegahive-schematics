# MCP interface
> Seam-register card. Code refs are to `omegahive` @ 34b0fb3 unless another repo is named. Back to the [register](README.md).

## What it does
Lets outside agents (Claude Code, Codex or any MCP client) join a swarm as members. An admin makes a one-time invite code; the client connects to `/mcp` with the member token and gets a fixed set of hive tools. Their tool calls go through `Policy.enforce`, the same rules native minds are judged by; external members do not get the native loop's local skip list (K10). Unknown skills still default to allow (K30).

Upstream: [MCP and agent interop](https://github.com/PhysixSNET/omegahive-start-here/blob/main/ACKNOWLEDGEMENTS.md#mcp-and-agent-interop).

## Where it lives
- `hive/core/mcp.py:221` `Harnesses`: `invite` `:237`, `member` `:282`, `rate_ok` `:305`, `handle` `:317`, `call` `:442`.
- Tool list `hive/core/mcp.py:87-150`; a built but gated-off tool `GATED` `:151`.
- Endpoint `hive/core/app.py:652-676`; invite routes `:629-647`.
- Published schema: `hive/MCP_S3.md` (schema `s3-r1`); joining guide `hive/JOINING.md`.

## Contract at its edge
- **Transport:** MCP over streamable HTTP, JSON responses only, `POST /mcp`, `Authorization: Bearer <member token>`; `protocolVersion` `2025-06-18` (`MCP_S3.md:8-9`).
- **Limits:** 120 calls per member per 60 seconds (`mcp.py:305-313`), 256 KB per request, batches of at most 20 (`app.py:663-672`).
- **Tools:** `hive_whoami`, `hive_inbox`, `hive_send`, `hive_goals`, `hive_goal_*`, `hive_exhibit_read`, `hive_revision_read`, `hive_artifact_read`, `hive_request`, `hive_motivation_create`, `hive_motivations`, `hive_capabilities`, `hive_publish`, `hive_query`, `hive_evidence_query`; with the omegahive pull request `port/repo-map-host`, `hive_repo_query` (read-only repository maps, judged as the `repo-query` skill: `hive/core/mcp.py:149`, `:172`, `:711`).
- **Errors:** JSON-RPC codes -32001 (bad code), -32002 (rate), -32600, -32700.

## Status and known issues
**Built.** `STATUS.md:30`. `hive_evidence_publish` is built but gated off (`MCP_S3.md:50`). The `hive_capabilities` description still says the boot-receipt seam has not landed (`mcp.py:137`), but the handler already returns the inventory (`mcp.py:635-640`); the text is stale.

## Tests that guard it
`hive/tests/test_mcp_api.py`, `test_mcp_s3.py` (schema and gating), `test_share_body_through_harness.py`, `test_policy_hive_skills.py`.

## Swap point
**Yes**, for the tool set; the transport is standard MCP. A replacement or extension must keep tool names and `inputSchema` exactly, or bump the schema tag. Conformance test: `hive/tests/test_mcp_s3.py` checks the published schema; there is no client-side conformance kit yet.

## Equivalent in the SingularityNET stack
Option to evaluate: publishing hive tools as services through the SingularityNET marketplace daemon, so outside agents can find and pay for them. This would sit beside MCP, not replace it.

## Keep criteria
Keep if the generated `MCP_S3.md` matches `tools/list` byte for byte in CI, and every tool passes through the same policy gate as the native skill.

## Read next
[03-minds/04-channels-and-external-members](../03-minds/04-channels-and-external-members.md), [05-governance/01-permissions-and-policy](../05-governance/01-permissions-and-policy.md), 09-security-and-launch/01-threat-model, TB7 (in the private omegahive-security repo; ask Kabir), [10-testing/01-test-map](../10-testing/01-test-map.md#components-and-their-tests).
