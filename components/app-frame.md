# App frame
> Seam-register card. Code refs are to `omegahive` @ 34b0fb3 unless another repo is named. Back to the [register](README.md).

## What it does
Shows an app's own interface (its `ui/` folder) inside a sandboxed iframe. The app talks to the host only through `postMessage` on a per-frame channel, with rate limits. The host answers reads, opens files and URLs after checks, starts goals, and asks the person to confirm acts.

## Where it lives
- `hive/ui/src/features/programs/AppFrame.tsx`: iframe with `sandbox="allow-scripts allow-downloads"` `:386`; send `:145`; message handling `:205-287`; listener `:334`.
- `hive/ui/src/lib/appFrame.ts` (`appDocument` `:34`, CSP meta `:26`, `isFrameSender` `:51`), `lib/appBridge.ts` (`appContext` `:121`, `parseBridgeMessage` `:181`, `BRIDGE_LIMITS` `:213`), `lib/frameOps.ts` (`FRAME_OP_LIMITS` `:45`, `parseFrameOp` `:111`), `lib/hostConfirm.ts`.
- Server: `hive/core/ui_parts.py:1-10` (rules for a UI that declares scripts); bundle route `GET /api/programs/{id}/ui` (`hive/core/app.py:2855-2858`).
- Contract text: `hive/PROGRAMS.md` §9 to §9d.

## Contract at its edge
- **Messages from the app:** `app-ready`, `context?`, `pick`, `subscribe`, `unsubscribe`, `read`, `open-url`, `show-file`, `back`, `layout`, `goal`, `app-dirty`; each carries the frame's `channel`.
- **Limits:** for example `context?` 10 per 10 s, `read` 30 per 10 s (`appBridge.ts:213`, `frameOps.ts:45`).
- **Integrity:** the UI bundle must match its lock and the app's pin, or it stays closed with 403 `app_integrity` (`hive/core/programs.py:747,857`).

## Status and known issues
**Built.** Several §9 sections are marked candidate additions in `PROGRAMS.md`.

## Tests that guard it
UI: `lib/appBridge.test.ts`, `appFrame.test.ts`, `appFrame.browser.test.ts`, `frameOps.test.ts`, `frameIdentity.test.ts`, `studioBridge.test.ts`, `features/programs/HostConfirm.test.ts`, `frameAct.test.ts`. Hive: `hive/tests/test_app_ui.py`, `test_app_ui_parts.py`.

## Swap point
**Yes**, for apps: any app UI that speaks the §9 messages works. The host side is not meant to be swapped. Conformance test: none yet for an app UI, write one first.

## Equivalent in the SingularityNET stack
No direct equivalent.

## Keep criteria
Keep if a browser test shows the frame cannot reach the host origin, storage or network beyond the CSP, and every op is rate-limited and identity-bound.

## Read next
[02-ask-and-ui/03-app-frame-bridge](../02-ask-and-ui/03-app-frame-bridge.md), [06-apps/01-programs-contract](../06-apps/01-programs-contract.md), 09-security-and-launch/01-threat-model, TB2 (in the private omegahive-security repo; ask Kabir), [08-reviewers/03-review-checklists, UI](../08-reviewers/03-review-checklists.md#10-ui-experiences-and-the-app-frame), [10-testing/01-test-map](../10-testing/01-test-map.md#components-and-their-tests).
