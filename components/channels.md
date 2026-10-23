# Channels
> Seam-register card. Code refs are to `omegahive` @ 34b0fb3 unless another repo is named. Back to the [register](README.md).

## What it does
How a mind talks to the outside world. Hive minds use one channel, the hive channel, which carries messages over the [agent hub](agent-hub.md). The inherited runtime also has adapters for Telegram, WhatsApp, Mattermost, Slack, IRC, a web control page and a mock. These are not wired for hive minds by design.

Upstream: [channels](https://github.com/PhysixSNET/omegahive-start-here/blob/main/ACKNOWLEDGEMENTS.md#channels), [OmegaClaw Core](https://github.com/PhysixSNET/omegahive-start-here/blob/main/ACKNOWLEDGEMENTS.md#omegaclaw-core).

## Where it lives
- Hive channel: `modules/channel_hive/module.toml` (provides `channel:hive`; settings `HIVE_WS_URL`, `HIVE_WS_TOKEN`), `modules/channel_hive/src/hive_channel.py`.
- Choice for hive minds: `COMMCHANNEL = "hive"` at `hive/supervisor/workspace.py:34`; loop branches at `src/loop.metta:74,115`; `initChannels` at `src/loop.metta:145`.
- Other adapters: `channels/*.py` (`telegram.py`, `whatsapp.py`, `mattermost.py`, `slack.py`, `irc.py`, `web_control.py`, `mock.py`, router `channels/router.py`), and module wrappers `modules/channel_*`.
- Closed tier: `channels/whatsapp_bridge` and `modules/channel_whatsapp/src/whatsapp_bridge` (GPL-3 dependency, `docs/MODULARITY.md:20`).

## Contract at its edge
- **Adapter functions:** `start_<name>(...)`, `getLastMessage()`, optional `getLastEvents()`, `send_message(str)` (`docs/reference-channels.md:11-16`; a current contract).
- **Event shape:** `CHANNEL_EVENT` with `event`, `channel`, `route`, `conversation_id`, `message_id` and more (`docs/reference-channels.md:18-30`).
- **Module manifest:** `kind = "channel"` in `module.toml`, with `provides`, `requires`, `[env.*]` and `[trace]`.

## Status and known issues
**Partial.** The hive channel is built. Other channels are in the core but unused by hive minds (`STATUS.md:59`), and their compatibility with this hive is untested (`STATUS.md:76`).

## Tests that guard it
Runtime: `tests/test_channel_hive.py`, `test_channel_hive_runtime.py`, `test_channel_event_normalization.py`, `test_syntax_channels_smoke.py`, `test_telegram_send_guard.py`, `test_whatsapp_jid_guard.py`. Hive: `hive/tests/test_channel_launch.py`.

## Swap point
**Yes.** A new channel is a module with `kind = "channel"`. Conformance test: `tests/test_module_contract.py` for the manifest; `tests/test_channel_event_normalization.py` for event shape. Guide: `docs/tutorial-04-adding-a-channel.md`.

## Equivalent in the SingularityNET stack
No direct equivalent known to this author.

## Keep criteria
Keep the hive channel as is. For any other channel at launch, require a fresh test run against this hive and a policy review, because it leaves the hive's boundary.

## Read next
[03-minds/04-channels-and-external-members](../03-minds/04-channels-and-external-members.md), [03-minds/03-modules](../03-minds/03-modules.md), 09-security-and-launch/01-threat-model, TB8 (in the private omegahive-security repo; ask Kabir), 07-upgrade-path/FINDINGS, K60 to K62 (in the private omegahive-security repo; ask Kabir), [10-testing/01-test-map](../10-testing/01-test-map.md#components-and-their-tests).
