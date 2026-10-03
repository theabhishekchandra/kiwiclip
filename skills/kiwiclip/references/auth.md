# Authenticated recording — security rules

This is the part of `/kiwiclip` that `/brag`-style skills don't need, because they only ever touch public marketing pages. Recording behind a login means handling real credentials, and every rule below exists to make sure that goes nowhere it shouldn't.

## Where credentials come from

**Never** from inline chat text that this skill would echo back. Acceptable sources, in order of preference:

1. Environment variables already set in the user's shell: `KIWICLIP_EMAIL`, `KIWICLIP_PASSWORD`, `KIWICLIP_TOTP_SECRET`.
2. A local file `.kiwiclip/credentials.env` (add it to `.gitignore` if it isn't already) that the user created themselves, read at runtime.

If the user pastes a password or token directly into the conversation, stop, tell them to move it to one of the sources above instead, and don't repeat the value back in any form (not even partially).

## v1 supported auth

| Type | How |
|---|---|
| Email + password | `scripts/record.py` fills the form, submits, waits for `post_login_url_contains` |
| TOTP / 2FA | `scripts/record.py` generates the current code with `pyotp.TOTP(secret).now()` from `KIWICLIP_TOTP_SECRET`, right when the OTP field appears — the secret is read from the environment, never written to `plan.json` |
| Session cookie import | Not yet wired into `record.py` — deferred alongside the other auth types below until someone needs it |

`record.py` imports `validate_url_for_recording` directly from `validate_url.py` (not a subprocess call) and runs it on both the login URL and every `goto` target before navigating — see [step-3-record.md](step-3-record.md) for the full plan.json shape.

**Deferred, not v1** — OAuth popup flows, SSO/SAML, magic-link-via-email-polling, SMS OTP interception, multi-role batch recording. Each adds real complexity (a popup handler, an IdP redirect, an email API, a second phone number) for a secondary case. Build the core loop solid first; see [roadmap.md](roadmap.md) for the sequencing.

## SSRF validation

Run every URL — login URL and product URL — through `scripts/validate_url.py` before navigating. It blocks `localhost`, `127.0.0.1`, cloud metadata endpoints (`169.254.169.254`), and private IP ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`). This matters even for a tool that "just runs on your own machine" — the browser doing the navigating can still be pointed at your own internal network by a malicious or mistaken URL.

## Session handling

- `record.py` saves Playwright's `storage_state` to `<output-dir>/.session/state.json` — scoped to that one job's output directory (which `.gitignore` already excludes), not a shared location reused across unrelated jobs.
- If a session file already exists for that output directory, it's reused instead of logging in again. Delete the output directory (or just its `.session/` subfolder) when you're done with a job to clear it.
- Never log cookie or token values, even at debug verbosity.

## Masking

See [step-3-record.md](step-3-record.md) — the mask must be injected before the first navigation, not patched in after a frame has already rendered the secret.

## One role per job in v1

If the user needs both an admin demo and a user demo, run `/kiwiclip` twice with different credentials rather than batching roles in one job. Batched multi-role recording is a later-phase feature (see [roadmap.md](roadmap.md)) — it mainly saves setup time, which matters more once this is already working reliably for one role.
