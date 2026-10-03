# Step 2 — Plan

Write `<output-dir>/plan.md` containing:

1. **Narration script** — plain text at this stage (SSML pacing gets added in Step 4). Conversational, specific to this product, ~140 words/minute pace. No generic marketing language (see [creative-laws.md](creative-laws.md)).
2. **Browser action list** — the concrete, ordered steps: `goto`, `click`, `fill`, `scroll`, each with a human-readable target description (not just a raw selector — the selector gets resolved at record time via the locator strategy in [step-3-record.md](step-3-record.md)).
3. **Scene plan** — one scene per screen/action, each with an estimated duration in seconds.
4. **Tone** — `walkthrough`, `tutorial`, `marketing-demo`, or the user's freeform direction.

## Target length

Unlike a 15–25s launch-hype clip, a demo walkthrough's job is instructional clarity, not a hook. Default target: **45–120 seconds**, scaled to how many steps the flow actually has — don't pad a 3-step flow to 90 seconds, and don't cram a 10-step flow into 45. `--duration` overrides the default if the user gives one.

## Tone presets

| Tone | Pace | Use for |
|---|---|---|
| `walkthrough` | Calm, steady holds, full narration | Default — explaining a real flow |
| `tutorial` | Slower, numbered steps, pauses for reading | Onboarding docs, support articles |
| `marketing-demo` | Faster cuts, shorter (~30–45s), more energy | Launch pages, social teasers |

Freeform direction always overrides a preset's specifics while keeping its structural shape.

**Gate:** `plan.md` exists. Scene durations sum to the target window (±10%). Every scene maps to a step from the action list — nothing vague like "then show the dashboard."
