# Step 4 — Compose

Everything in this step runs with on-machine tools (`ffmpeg`, a TTS API call, Whisper) via `scripts/narrate.py`, `scripts/caption.py`, and `scripts/compose.py`. No bundled rendering engine, no Remotion project to maintain.

## 1. Narration (only if voice is on — the default)

```bash
python3 <skill-dir>/scripts/narrate.py <output-dir>/narration_script.txt <output-dir>/narration.mp3
```

Write `narration_script.txt` from the plan — plain text, SSML-style pacing is handled by the TTS provider's own prosody, so keep the text natural ("Here you can...", short sentences, one idea per sentence). The script checks `ELEVENLABS_API_KEY` first, falls back to `OPENAI_API_KEY`, and fails loudly if neither is set rather than producing a silent track.

Skip this step entirely for `--no-voice`.

## 2. Captions (on by default)

```bash
python3 <skill-dir>/scripts/caption.py <output-dir>/narration.mp3 <output-dir>/captions.srt
```

Pinned to OpenAI's `whisper-1` deliberately — it's the one OpenAI transcription model that still supports word-level timestamps with SRT export (the newer `gpt-transcribe` is more accurate overall but dropped that capability). See the comment at the top of `caption.py` before "upgrading" this.

Skip for `--no-captions`, or if voice is off and there's no narration audio to transcribe.

## 3. Compose

```bash
python3 <skill-dir>/scripts/compose.py <output-dir>/raw/recording.webm <output-dir> \
  --steps-log <output-dir>/steps_log.json \
  --narration <output-dir>/narration.mp3 \
  --music <output-dir>/music.mp3 \
  --captions <output-dir>/captions.srt
```

Omit `--narration` / `--music` / `--captions` entirely for whichever stages weren't produced above — their absence is what turns each stage off, there's no separate boolean flag to keep in sync.

What it does:

- A gentle continuous zoom across the whole clip (not per-element yet — frame-accurate per-element highlight boxes need precise step timestamps aligned to the recording, which is a fast-follow; see [roadmap.md](roadmap.md)).
- A lower-third step label per recorded step, evenly spaced across the runtime, text pulled from `steps_log.json`.
- If `--narration` is given: mixes it in; if `--music` is also given, ducks the music under the voice with `sidechaincompress` (voice stays dominant, music drops under it automatically rather than needing manual levels).
- If `--captions` is given: burns in the `.srt` with a readable default style (white text, dark box, bottom-centered).

Output: `<output-dir>/composed.mp4`.

## Why music defaults off here

A product demo's job is to be understood. Background music is one more thing competing with the narration for attention — the opposite trade-off from a 20-second hype reel. Only add `--music` if the user asks for it, and keep the duck aggressive enough that it never competes with the voice.

**Gate:** `<output-dir>/composed.mp4` exists. Spot-check it plays and the label timing roughly lines up with the action before moving to Step 5 — `export.py`'s `ffprobe` validation catches structural problems (missing audio, wrong resolution, black frames) but not "does this look right."
