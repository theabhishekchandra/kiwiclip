#!/usr/bin/env python3
"""Transcribe narration audio into word-timed captions for /kiwiclip.

Usage:
    python3 caption.py <audio.mp3> <output.srt>

Deliberately pinned to OpenAI's `whisper-1`, NOT the newer gpt-transcribe
family. As of this writing, whisper-1 is the only OpenAI transcription model
that supports word-level timestamps with SRT export, which is exactly what
burned-in karaoke-style captions need -- gpt-transcribe is more accurate but
drops that capability. Don't "upgrade" this without checking that first.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from openai import OpenAI


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: caption.py <audio.mp3> <output.srt>", file=sys.stderr)
        sys.exit(2)

    if not os.environ.get("OPENAI_API_KEY"):
        print(
            "OPENAI_API_KEY is not set. Captions always use OpenAI's Whisper for "
            "word-level timestamps, even if ElevenLabs is the narration provider. "
            "Set OPENAI_API_KEY, or run with --no-captions.",
            file=sys.stderr,
        )
        sys.exit(1)

    audio_path, output_path = Path(sys.argv[1]), Path(sys.argv[2])
    client = OpenAI()

    with open(audio_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="srt",
            timestamp_granularities=["word"],
        )

    output_path.write_text(transcript if isinstance(transcript, str) else transcript.text)
    print(str(output_path))


if __name__ == "__main__":
    main()
