#!/usr/bin/env python3
"""Export final format(s), a thumbnail, and validate the output for /kiwiclip.

Usage:
    python3 export.py <composed.mp4> <output-dir> [--formats 16x9,9x16,1x1] [--expect-audio]

Note on the thumbnail: rather than attempting to literally replace frame 0 of
the video stream (fragile with re-encode/sync risk for a cosmetic gain), this
picks a frame and saves it as a standalone `thumbnail.jpg`. Every platform
this skill writes copy for (YouTube, LinkedIn, a docs embed) takes a thumbnail
as a separate upload/`poster` attribute, so this covers the real goal
reliably. True frame-0 baking is a tracked fast-follow, not a v1 claim -- see
references/roadmap.md.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

FORMAT_SPECS = {
    "16x9": {"w": 1920, "h": 1080},
    "9x16": {"w": 1080, "h": 1920},
    "1x1": {"w": 1080, "h": 1080},
}


def run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True)


def run_ffmpeg(args: list[str]) -> None:
    result = run(["ffmpeg", "-y", *args])
    if result.returncode != 0:
        print(result.stderr[-4000:], file=sys.stderr)
        raise RuntimeError(f"ffmpeg failed: {' '.join(args[:4])}...")


def export_format(src: Path, dst: Path, fmt: str) -> None:
    spec = FORMAT_SPECS[fmt]
    vf = f"scale={spec['w']}:{spec['h']}:force_original_aspect_ratio=decrease,pad={spec['w']}:{spec['h']}:(ow-iw)/2:(oh-ih)/2"
    run_ffmpeg(["-i", str(src), "-vf", vf, "-c:v", "libx264", "-crf", "18", "-preset", "fast",
                "-c:a", "aac", "-b:a", "192k", str(dst)])


def extract_thumbnail(src: Path, dst: Path, duration: float) -> None:
    timestamp = max(duration * 0.4, 0.5)
    run_ffmpeg(["-i", str(src), "-ss", f"{timestamp:.2f}", "-vframes", "1", "-q:v", "2", str(dst)])


def probe(path: Path) -> dict:
    result = run(["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", "-show_format", str(path)])
    return json.loads(result.stdout)


def black_frame_ratio(path: Path, duration: float) -> float:
    result = run(["ffmpeg", "-i", str(path), "-vf", "blackdetect=d=0.5:pix_th=0.10", "-f", "null", "-"])
    black_total = 0.0
    for match in re.finditer(r"black_duration:([\d.]+)", result.stderr):
        black_total += float(match.group(1))
    return black_total / duration if duration > 0 else 0.0


def validate(path: Path, fmt: str, expect_audio: bool) -> list[str]:
    data = probe(path)
    streams = data.get("streams", [])
    video_stream = next((s for s in streams if s["codec_type"] == "video"), None)
    audio_stream = next((s for s in streams if s["codec_type"] == "audio"), None)
    duration = float(data.get("format", {}).get("duration", 0))
    spec = FORMAT_SPECS[fmt]

    failed = []
    if video_stream is None:
        failed.append("has_video")
    else:
        if (video_stream.get("width"), video_stream.get("height")) != (spec["w"], spec["h"]):
            failed.append("correct_resolution")
        if video_stream.get("codec_name") not in ("h264", "h265"):
            failed.append("codec_correct")
    if expect_audio and audio_stream is None:
        failed.append("has_audio")
    if duration > 0 and black_frame_ratio(path, duration) > 0.05:
        failed.append("no_black_frames")
    return failed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("composed_video")
    parser.add_argument("output_dir")
    parser.add_argument("--formats", default="16x9")
    parser.add_argument("--expect-audio", action="store_true")
    args = parser.parse_args()

    src = Path(args.composed_video)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    formats = [f.strip() for f in args.formats.split(",") if f.strip()]

    duration = float(probe(src).get("format", {}).get("duration", 0))

    thumbnail = output_dir / "thumbnail.jpg"
    extract_thumbnail(src, thumbnail, duration)

    results = {}
    all_failed: dict[str, list[str]] = {}
    for fmt in formats:
        if fmt not in FORMAT_SPECS:
            print(f"Unknown format '{fmt}', skipping. Known: {list(FORMAT_SPECS)}", file=sys.stderr)
            continue
        dst = output_dir / f"video_{fmt}.mp4"
        export_format(src, dst, fmt)
        failed = validate(dst, fmt, args.expect_audio)
        results[fmt] = str(dst)
        if failed:
            all_failed[fmt] = failed

    if all_failed:
        print(json.dumps({"status": "failed", "videos": results, "thumbnail": str(thumbnail), "failed_checks": all_failed}))
        sys.exit(1)

    print(json.dumps({"status": "ok", "videos": results, "thumbnail": str(thumbnail)}))


if __name__ == "__main__":
    main()
