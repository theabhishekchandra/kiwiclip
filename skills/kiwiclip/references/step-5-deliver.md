# Step 5 — Deliver

## Export and validate

```bash
python3 <skill-dir>/scripts/export.py <output-dir>/composed.mp4 <output-dir> \
  --formats 16x9 \
  --expect-audio
```

- `--formats` is a comma list from `16x9` (default), `9x16`, `1x1` — only render what `--format` on the invocation actually asked for; don't spend render time on formats nobody requested.
- Pass `--expect-audio` whenever voice or music was on in Step 4, so the validator fails loudly if the audio track is silently missing instead of shipping a mute video.

The script writes `video_<format>.mp4` for each requested format, a `thumbnail.jpg`, and exits non-zero with the specific failing checks (`has_video`, `has_audio`, `correct_resolution`, `codec_correct`, `no_black_frames`) if validation fails. **A failed export doesn't get shipped** — fix the underlying issue (usually something upstream in Step 4) and re-run, rather than delivering a video with a caveat attached.

## Thumbnail, honestly

`export.py` picks a frame and saves it as a standalone `thumbnail.jpg` — it does not attempt to splice that frame in as literal frame 0 of the `.mp4`. Every platform this skill writes copy for (YouTube, LinkedIn, a docs embed) takes a thumbnail as a separate upload or `poster` attribute, so a standalone file covers the real goal reliably. True frame-0 baking is fragile (re-encode + sync risk for a cosmetic gain) and is a tracked fast-follow in [roadmap.md](roadmap.md), not a v1 claim this skill makes.

## Platform copy

Write markdown files under `<output-dir>/posts/` for exactly the platforms in `--platforms` (default `youtube,linkedin,embed`):

- `youtube.md` — title, description with timestamps (pull timestamps from `steps_log.json`), tags.
- `linkedin.md` — a caption in a professional tone, no generic marketing language.
- `embed.md` — a one-paragraph caption suited for a docs page or README, since many demo videos live there, not on social.
- `twitter.md` — only if requested — single tweet + optional short thread.

This is a deliberately short list. The original research considered twelve platforms (Product Hunt, Hacker News, Reddit, Dev.to, email, Slack...) — real, but belongs to a later phase once the core loop is solid; see [roadmap.md](roadmap.md). Add more via `--platforms` only when asked. These are plain markdown files the agent writes directly (no script needed — this is exactly the kind of content generation the orchestrating agent does itself, not a mechanical script).

## Never publish

This skill does not call any posting API, ever, in any phase of v1. It writes files. If the user wants to post, that's their action with their own tools and their own account.

## Final output layout

```
<output-dir>/
├── plan.md
├── plan.json
├── raw/recording.webm
├── steps_log.json
├── composed.mp4
├── video_16x9.mp4            (+ video_9x16.mp4 / video_1x1.mp4 if requested)
├── thumbnail.jpg
├── captions.srt              (if captions on)
└── posts/
    ├── youtube.md
    ├── linkedin.md
    └── embed.md
```

**Gate:** every file above exists for what was requested. Tell the user where the output is, the creative angle taken, and that nothing was posted anywhere.
