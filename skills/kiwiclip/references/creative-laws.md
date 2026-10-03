# Creative laws

These apply to every video this skill produces, regardless of tone. They're the direct answer to the "robotic QA test, not a marketing asset" problem this skill exists to solve.

**Clarity over hype.** The test isn't "does this look exciting" — it's "could someone repeat this workflow after watching once." If a viewer can't, the video failed regardless of how polished it looks.

**Show the real product.** Real cursor movement, real clicks, real screens, real data where possible. Never fabricate a UI state, never stage a result that the product didn't actually produce.

**Narrate the why, not just the what.** "Click here" describes the UI. "This saves your team a manual export every week" describes the value. Always prefer the second. Pull the *why* from the product's own docs/copy — don't invent a benefit it doesn't have.

**Readable pacing.** Any line of narration or caption a viewer is meant to read stays fully visible for its natural reading time — roughly 0.3 seconds per word, counted from when the full line is on screen, not from when it starts appearing. Hold each distinct UI action for about 1.5–2.5 seconds before cutting, long enough to register what happened.

**Match video pacing to narration, not the reverse.** Don't speed up narration to fit a cut; extend the hold.

**Zero tolerance on secrets.** Any frame containing a visible password, API key, token, or OTP value fails the gate completely. There is no "blur it in post" fallback — mask before recording (see [step-3-record.md](step-3-record.md)) and re-record if a leak is found, don't ship it and hope.

**No generic marketing language.** "Streamline your workflow," "unlock your potential," "supercharge your team" are all banned. Describe the specific action the product just took on screen.

**One real flow beats five shallow ones.** A focused 60-second walkthrough of the flow that actually matters beats a 3-minute tour that touches everything and explains nothing well.

**Funny, if it happens, comes from the product, not from trying.** Most demo walkthroughs shouldn't be funny at all — that's fine. If `marketing-demo` tone leans playful, the humor should come from something genuinely surprising or delightful about the product, not from jokes bolted on top.
