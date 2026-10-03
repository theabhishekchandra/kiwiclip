# Roadmap — what's deferred, and why

`kiwiclip_research.md` in the repo root captured a much larger vision: mobile capture, multi-language dubbing, AI b-roll, auto-publishing to twelve platforms, an async job queue, a hosted credential vault. All of that is good material — it's just the wrong scope for a v1 *skill* that runs inline in someone's agent session. A skill that takes 6–11 weeks to become minimally useful won't get used. This file keeps the ambition on record and sequences it after the core loop actually works.

## Shipped in v1 (this skill, as scaffolded)

- Local project or live URL inspection, including one authenticated flow (email/password + TOTP).
- Planned, verified browser recording with secret masking.
- Zoom/highlight annotation, narration (on by default), burned-in captions.
- Single-format export by default, multi-format on request.
- Platform copy as local files. No posting, ever.

## Phase 2 — Broaden authenticated recording

- OAuth popup handling (Google/GitHub), SSO/SAML, magic-link-via-email-polling, SMS OTP.
- Full authenticated-sitemap auto-discovery (crawl every route behind login, AI-rank by demo priority) — v1 only records the 3–4 screens the user confirms.
- Multi-role batch recording (admin + user in one invocation).

*Why deferred:* each auth type is a real integration (a popup handler, an IdP redirect flow, an email API) for a case most users won't hit on day one. Ship the common path first.

## Phase 3 — Format and reach

- Multi-language dubbing (lip-sync via a provider like HeyGen, or audio-only via the TTS provider already in use).
- The full twelve-platform copy set (Product Hunt, Hacker News, Reddit, Dev.to, newsletter, Slack/WhatsApp) — v1 ships `youtube`, `linkedin`, `embed`, optional `twitter`.
- AI-generated b-roll for scenes with no UI to show.

*Why deferred:* these add vendor integrations and cost per run without changing whether the core video is any good. Better to nail quality first, then widen reach.

## Phase 4 — Mobile

- Android capture (ADB + Appium/UiAutomator2) and iOS capture (`xcrun simctl` + Appium/XCUITest), behind the same `MobileCaptureBase` contract shape sketched in the original research.

*Why deferred:* an entirely separate capture stack from Playwright. Only worth building once the web path is reliable enough that people actually ask for the mobile equivalent.

## Phase 5 — Scale, if ever needed

- Async job queue, webhook/SSE progress, checkpointed resumable pipeline, hosted CDN delivery.

*Why deferred, maybe permanently:* this only matters if `/kiwiclip` becomes a *hosted service* (the way letsbrag.app hosts `/brag`) rather than a skill people run locally. If that day comes, build it as a separate hosted product on top of this skill — not as the skill's own architecture. A skill that needs Redis to run isn't something people can `git clone` and use in five minutes.

## Explicitly never (unless the user asks for a different product)

- Posting to any platform API from inside this skill. Even with a confirmation step, that's a different trust model than "writes files to your disk." If auto-publish is ever wanted, it should be an opt-in companion tool the user installs separately and reviews on its own — not bundled into the default `/kiwiclip` invocation.
