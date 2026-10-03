# Step 3 — Record

Basic `fill()` + `click()` automation breaks the moment a button ID changes or a modal blocks the screen — and it fails *silently*, producing a corrupted recording nobody notices until playback. `scripts/record.py` runs every planned action through an observe → act → verify loop instead of fire-and-forget, and masks sensitive fields before the first frame is captured.

## Write the plan as JSON

Turn the `plan.md` from Step 2 into `<output-dir>/plan.json` — this is what `record.py` actually executes:

```json
{
  "login": {
    "login_url": "https://app.example.com/login",
    "post_login_url_contains": "dashboard"
  },
  "steps": [
    { "action": "goto", "url": "https://app.example.com/dashboard" },
    { "action": "click", "hint": "Create project", "role": "button" },
    { "action": "fill", "hint": "Project name", "value": "Demo project" },
    { "action": "scroll", "y": 500 },
    { "action": "wait", "ms": 1000 }
  ]
}
```

Omit `login` entirely for a public, unauthenticated flow. `hint` is a human-readable description of the target element — `record.py` resolves it through a locator fallback chain (role → label → placeholder → text → test id), not a raw CSS selector, so it survives minor UI changes.

## Run it

```bash
python3 <skill-dir>/scripts/record.py <output-dir>/plan.json <output-dir>
```

Credentials for the `login` block come from `KIWICLIP_EMAIL` / `KIWICLIP_PASSWORD` / `KIWICLIP_TOTP_SECRET` in the environment — see [auth.md](auth.md). The script refuses to run without them rather than prompting for a value it would then have to handle.

What it does, per step, automatically:

1. **Mask first.** The password/OTP/card-field CSS mask is injected via `context.add_init_script(...)` before any navigation — not patched in afterward. A mask applied after the page has already rendered a frame is too late; that frame is already in the recording.
2. **Observe → act → verify.** Every step checks page state before and after, retries up to 3 times with backoff (500ms/1.5s/3s) on failure, and auto-recovers from a cookie banner by clicking the first visible `Accept`/`Got it`/`I agree` button.
3. **Locator fallback chain**, most to least resilient: role → label → placeholder → text → test id. If every strategy fails, the script exits non-zero with a screenshot path (`<output-dir>/failure.png`) rather than guessing a raw CSS selector or guessing silently — look at the screenshot, give the step a better `hint`, and re-run.
4. **Session re-auth.** If a step redirects back to `/login` mid-flow, the script raises rather than continuing to record a broken state.
5. **Human-like movement.** The mouse eases toward each clicked element across several steps rather than teleporting — a demo of real usage should look like a human used it. (This is a simple hand-rolled interpolation, not a full ghost-cursor port — good enough for v1; see [roadmap.md](roadmap.md).)

On success it writes `<output-dir>/raw/recording.webm` and `<output-dir>/steps_log.json` (used by `compose.py` for step labels, and by `privacy_scan.py`'s context). On failure it prints a JSON error with the screenshot path and exits 1 — don't proceed to Step 4 on a non-zero exit.

## Privacy scan — before moving on

```bash
python3 <skill-dir>/scripts/privacy_scan.py <output-dir>/raw/recording.webm
```

If it prints `PASSED`, proceed. If it prints `FAILED`, the listed frames contain something that looks like a secret — re-record after fixing the mask or the flow, don't ship it. If it prints `SKIPPED` (OCR tooling not installed), that is **not** a pass — ask the user to glance at a few frames of the recording themselves before proceeding, and say plainly that the automated scan didn't run.

**Gate:** a recording exists for every planned screen. No step failed verification. The privacy scan passed, or was explicitly skipped with the user told so.
