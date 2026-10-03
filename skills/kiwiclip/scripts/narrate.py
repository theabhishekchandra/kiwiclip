#!/usr/bin/env python3
"""Synthesize narration audio for /kiwiclip.

Usage:
    python3 narrate.py <script.txt> <output.mp3> [--voice NAME]

Picks a TTS provider based on which API key is set in the environment --
ELEVENLABS_API_KEY first (best quality), OPENAI_API_KEY as a fallback. Fails
loudly if neither is set rather than silently writing a silent track.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

DEFAULT_ELEVENLABS_VOICE = "Rachel"
DEFAULT_OPENAI_VOICE = "alloy"


def synthesize_elevenlabs(text: str, output_path: Path, voice: str) -> None:
    from elevenlabs.client import ElevenLabs

    client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
    audio = client.text_to_speech.convert(
        voice_id=voice,
        model_id="eleven_turbo_v2_5",
        text=text,
        voice_settings={"stability": 0.5, "similarity_boost": 0.8, "style": 0.4, "use_speaker_boost": True},
    )
    with open(output_path, "wb") as f:
        for chunk in audio:
            if chunk:
                f.write(chunk)


def synthesize_openai(text: str, output_path: Path, voice: str) -> None:
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.audio.speech.create(model="gpt-4o-mini-tts", voice=voice, input=text)
    response.stream_to_file(str(output_path))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("script_path")
    parser.add_argument("output_path")
    parser.add_argument("--voice", default=None)
    args = parser.parse_args()

    text = Path(args.script_path).read_text().strip()
    if not text:
        print("Narration script is empty.", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output_path)

    if os.environ.get("ELEVENLABS_API_KEY"):
        synthesize_elevenlabs(text, output_path, args.voice or DEFAULT_ELEVENLABS_VOICE)
    elif os.environ.get("OPENAI_API_KEY"):
        synthesize_openai(text, output_path, args.voice or DEFAULT_OPENAI_VOICE)
    else:
        print(
            "No TTS provider configured. Set ELEVENLABS_API_KEY or OPENAI_API_KEY "
            "in the environment before running with --voice on.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(str(output_path))


if __name__ == "__main__":
    main()
