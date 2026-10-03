---
name: kiwiclip
description: Turn a web product — including screens behind a login — into a narrated, captioned demo walkthrough video, plus ready-to-paste platform copy. Use when someone says "/kiwiclip", "make a demo video of my product", "record a walkthrough of this app", "show how this feature works", or wants a product demo/explainer video from a URL or local project. Runs entirely on your machine with your own credentials and API keys — nothing is uploaded to a third party by default.
---

# /kiwiclip

You shipped a feature. Now show how it actually works.

`/kiwiclip` turns a product — a local project, a live URL, or a live URL behind a login — into a short, clear, narrated demo walkthrough video. It is narrow and opinionated: one real flow, shown accurately, explained well. No mobile, no auto-posting, no twelve-platform blast in v1 — see [references/roadmap.md](references/roadmap.md) for what's deliberately deferred and why.

## What this skill does

1. Inspects the product (code, live page, or live page + login) to understand the one flow worth showing.
2. Plans a narration script and a step-by-step browser action list.
3. Records the real UI performing those steps (Playwright), with secrets masked before the first frame is captured.
4. Composes: zoom/highlight annotations, narration audio, burned-in captions.
5. Validates the output, exports it, and writes platform copy — never posts it anywhere.

## Parsing the invocation

```
/kiwiclip
/kiwiclip https://app.example.com --login
/kiwiclip --tone tutorial --duration 90
/kiwiclip this. Focus on the onboarding flow only.
```

| Option | Values | Default |
|---|---|---|
| `--login` | flag | off — see [references/auth.md](references/auth.md) before ever using this |
| `--tone` | `walkthrough`, `tutorial`, `marketing-demo`, or freeform direction | `walkthrough` |
| `--format` | `16x9`, `9x16`, `1x1` (repeatable) | `16x9` only |
| `--duration` | seconds | auto, 45–120s depending on flow length |
| `--voice` | flag, or `--no-voice` to disable | **on** |
| `--music` | flag | off |
| `--captions` | flag, or `--no-captions` to disable | on |
| `--platforms` | comma list: `youtube,linkedin,twitter,embed` | `youtube,linkedin,embed` |
| `--mobile` | — | not implemented in v1; stop and point the user to `references/roadmap.md` |

Narration defaults **on** here — the opposite of a launch-hype skill's default. A demo walkthrough's job is to explain a real flow; silent b-roll doesn't do that. Music defaults **off** for the same reason: clarity over vibe. Both are one flag away from the other setting.

## Output directory

Default: `kiwiclip-output/`. If it already exists, use a timestamped variant generated once at the start of the run and reused for every path in it:

```
kiwiclip-output-2026-05-04-143022/
```

## Skill directory

`<skill-dir>` is the directory containing this `SKILL.md`. Bundled scripts live under `<skill-dir>/scripts/`. Don't guess an install path — a plugin install, a `~/.claude/skills/` copy, and this repo each put it somewhere different.

---

## Step 1: Inspect

**Read:** [references/step-1-inspect.md](references/step-1-inspect.md)

Determine the input type (local project / public URL / authenticated URL), gather enough material to understand the product, and pick the single flow worth demoing.

**Gate:** You can answer all 9 questions in the inspection rubric, and — if `--login` was requested — credentials were read from environment variables or an untracked local file, never from inline chat text.

---

## Step 2: Plan

**Read:** [references/step-2-plan.md](references/step-2-plan.md)

Write `<output-dir>/plan.md`: the narration script, the step-by-step browser action list, scene durations, and chosen tone.

**Gate:** `plan.md` exists. Scene durations sum to the target window. Every planned step maps to a concrete, locatable UI action — no "then show the rest of the app."

---

## Step 3: Record

**Read:** [references/step-3-record.md](references/step-3-record.md)
**Read (if `--login`):** [references/auth.md](references/auth.md)

Execute the planned steps with an observe → act → verify loop, not fire-and-forget clicks. Mask sensitive fields before recording starts.

**Gate:** A recording exists for every planned screen. No action silently failed. A privacy scan of the raw recording finds zero visible passwords, tokens, or OTP codes before you proceed to Step 4.

---

## Step 4: Compose

**Read:** [references/step-4-compose.md](references/step-4-compose.md)

Add zoom/highlight annotations for the acted-on element, generate narration audio (if voice is on), burn in captions (if on), mix in music (only if `--music`).

**Gate:** `ffprobe` validation passes — correct resolution per requested format, audio present if voice/music requested, no black frames, captions within ±150ms of the narration.

---

## Step 5: Deliver

**Read:** [references/step-5-deliver.md](references/step-5-deliver.md)

Export the requested format(s), pick and bake in a poster frame, write the platform copy files for the requested platforms.

**Gate:** `<output-dir>/video_<format>.mp4`, `thumbnail.jpg`, `captions.srt` (if captions on), and `posts/*.md` all exist. Tell the user where they are and that publishing anywhere is a manual step this skill never takes.

---

## Creative laws

Full rules: [references/creative-laws.md](references/creative-laws.md)

The short version:

- **Clarity over hype.** Someone should be able to repeat the workflow after one watch.
- **Show the real product.** Real cursor, real clicks, real screens. Never fabricate a UI state.
- **Narrate the why, not just the what.** "This saves your team a step because..." beats "Click here."
- **Readable pacing.** Any line of narration or caption stays on screen long enough to read (~0.3s/word), and holds on each distinct action for ~1.5–2.5s before the cut.
- **Zero tolerance on secrets.** Any frame with a visible password, token, or OTP fails the gate. Re-record, don't ship it.
- **No generic marketing language.** Describe the actual action taken, not "streamline your workflow."

## Security rules (always enforced)

Full rules: [references/auth.md](references/auth.md)

- Credentials come from environment variables or a local, gitignored file — never typed inline as a value this skill echoes back.
- Every URL is validated against localhost, private IP ranges, and cloud metadata endpoints before navigation.
- Sensitive fields are CSS-masked **before** recording starts, not patched afterward.
- Session state is written to a job-scoped temp path and discarded at job end — never committed, never logged.
- This skill never calls a social/video-platform API. It writes files. Publishing is the human's decision, every time.
