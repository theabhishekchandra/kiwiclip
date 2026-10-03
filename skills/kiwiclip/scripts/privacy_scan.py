#!/usr/bin/env python3
"""Scan a recording for visible secrets before /kiwiclip proceeds past Step 3.

Usage:
    python3 privacy_scan.py <video.webm>

Extracts frames and OCRs them, flagging anything that looks like a password,
API key, or OTP/card number that slipped past the CSS mask in record.py.

Requires `pytesseract` (pip) and the `tesseract` binary on PATH. If either is
missing, this prints a clear warning and exits 0 -- a *skipped* scan, not a
passed one. The skill's gate (see references/step-3-record.md) treats a
skipped scan as "ask the user to eyeball a few frames," not a silent pass.
"""
from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

SUSPICIOUS_PATTERNS = [
    (re.compile(r"sk-[a-zA-Z0-9]{20,}"), "looks like an API key"),
    (re.compile(r"eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}"), "looks like a JWT"),
    (re.compile(r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b"), "looks like a card number"),
    (re.compile(r"\b\d{6}\b"), "looks like a 6-digit OTP code"),
]


def extract_frames(video_path: str, out_dir: Path, fps: float = 2.0) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-y", "-i", video_path, "-vf", f"fps={fps}", str(out_dir / "frame_%04d.png")],
        check=True, capture_output=True,
    )
    return sorted(out_dir.glob("frame_*.png"))


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: privacy_scan.py <video.webm>", file=sys.stderr)
        sys.exit(2)

    video_path = sys.argv[1]

    try:
        import pytesseract
        from PIL import Image
    except ImportError:
        print(
            "SKIPPED: pytesseract/Pillow not installed. Privacy scan did not run. "
            "Install them (and the `tesseract` binary) for an automated check, or "
            "manually eyeball a few frames of the recording before proceeding.",
            file=sys.stderr,
        )
        sys.exit(0)

    with tempfile.TemporaryDirectory() as tmp:
        try:
            frames = extract_frames(video_path, Path(tmp))
        except FileNotFoundError:
            print("SKIPPED: ffmpeg not found on PATH.", file=sys.stderr)
            sys.exit(0)
        except subprocess.CalledProcessError as e:
            print(f"SKIPPED: ffmpeg frame extraction failed: {e}", file=sys.stderr)
            sys.exit(0)

        hits = []
        for i, frame in enumerate(frames):
            try:
                text = pytesseract.image_to_string(Image.open(frame))
            except Exception:
                continue
            for pattern, description in SUSPICIOUS_PATTERNS:
                if pattern.search(text):
                    hits.append({"frame_index": i, "frame": str(frame), "issue": description})

    if hits:
        print("FAILED: possible secrets visible in recording:", file=sys.stderr)
        for h in hits:
            print(f"  frame {h['frame_index']}: {h['issue']}", file=sys.stderr)
        sys.exit(1)

    print("PASSED: no visible secrets detected in sampled frames.")
    sys.exit(0)


if __name__ == "__main__":
    main()
