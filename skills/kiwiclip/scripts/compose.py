#!/usr/bin/env python3
"""Compose the annotated, narrated, captioned video for /kiwiclip.

Usage:
    python3 compose.py <raw_video> <output-dir> \\
        [--steps-log steps_log.json] [--narration narration.mp3] \\
        [--music music.mp3] [--captions captions.srt]

Builds one ffmpeg filter graph: a gentle continuous zoom for polish, plus a
lower-third step label per recorded step (evenly spaced across the runtime --
precise per-element highlight-box timing needs frame-accurate step
timestamps, which is a fast-follow, not a v1 blocker; see
references/roadmap.md). Audio stages only run if their input file is passed:
no --narration means no voice track, no --music means no music, no
--captions means no burned-in subtitles. This mirrors the SKILL.md options
table (--voice/--music/--captions) one level down, where the orchestrating
agent decides *whether* to produce narration.mp3/captions.srt at all before
calling this script.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run_ffmpeg(args: list[str]) -> None:
    result = subprocess.run(["ffmpeg", "-y", *args], capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr[-4000:], file=sys.stderr)
        raise RuntimeError(f"ffmpeg failed: {' '.join(args[:4])}...")


def probe_duration(video_path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", str(video_path)],
        capture_output=True, text=True, check=True,
    )
    return float(json.loads(result.stdout)["format"]["duration"])


def escape_drawtext(text: str) -> str:
    return text.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'").replace("%", "\\%")


def step_labels(steps_log_path: Path | None) -> list[str]:
    if not steps_log_path or not steps_log_path.exists():
        return ["Demo"]
    entries = json.loads(steps_log_path.read_text())
    labels = []
    for entry in entries:
        step = entry.get("step", {})
        label = step.get("hint") or step.get("action", "Step")
        labels.append(str(label)[:60])
    return labels or ["Demo"]


def build_annotation_graph(labels: list[str], duration: float, fps: int = 30) -> str:
    # d=1 is deliberate: zoompan's `d` is how many OUTPUT frames to hold per
    # INPUT frame, not a duration/frame-count knob. Setting it to the clip's
    # total frame count (an earlier bug here) multiplies output frames by
    # that count -- a 6s clip came out 841s long. d=1 plus a persistent `zoom`
    # expression gives one smoothly-zooming output frame per input frame.
    graph = f"[0:v]zoompan=z='min(zoom+0.0004,1.08)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':fps={fps}:s=1920x1080[z0]"
    window = duration / len(labels)
    current = "z0"
    for i, label in enumerate(labels):
        start, end = i * window, (i + 1) * window
        nxt = f"v{i + 1}"
        text = escape_drawtext(f"{i + 1}. {label}")
        graph += (
            f";[{current}]drawtext=text='{text}':fontsize=26:fontcolor=white:"
            f"box=1:boxcolor=0x4F46E5@0.65:boxborderw=12:x=40:y=h-90:"
            f"enable='between(t,{start:.2f},{end:.2f})'[{nxt}]"
        )
        current = nxt
    return graph, current


def mix_audio(narration: Path, music: Path | None, output_path: Path) -> None:
    if music is None:
        run_ffmpeg(["-i", str(narration), "-c:a", "copy", str(output_path)])
        return
    run_ffmpeg([
        "-i", str(narration), "-i", str(music),
        "-filter_complex",
        "[0:a]aformat=sample_rates=44100:channel_layouts=stereo[voice];"
        "[1:a]volume=0.3[music];"
        "[voice][music]sidechaincompress=threshold=0.01:ratio=8:attack=300:release=900:makeup=1[ducked];"
        "[voice][ducked]amix=inputs=2:duration=first:weights='2 1'[final]",
        "-map", "[final]", "-c:a", "aac", str(output_path),
    ])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("raw_video")
    parser.add_argument("output_dir")
    parser.add_argument("--steps-log", default=None)
    parser.add_argument("--narration", default=None)
    parser.add_argument("--music", default=None)
    parser.add_argument("--captions", default=None)
    args = parser.parse_args()

    raw_video = Path(args.raw_video)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    duration = probe_duration(raw_video)
    labels = step_labels(Path(args.steps_log) if args.steps_log else None)
    graph, out_label = build_annotation_graph(labels, duration)

    annotated = output_dir / "annotated.mp4"
    run_ffmpeg([
        "-i", str(raw_video), "-filter_complex", graph, "-map", f"[{out_label}]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-an", str(annotated),
    ])

    with_audio = output_dir / "with_audio.mp4"
    if args.narration:
        mixed_audio = output_dir / "mixed_audio.aac"
        mix_audio(Path(args.narration), Path(args.music) if args.music else None, mixed_audio)
        run_ffmpeg([
            "-i", str(annotated), "-i", str(mixed_audio),
            "-c:v", "copy", "-c:a", "aac", "-shortest", str(with_audio),
        ])
    else:
        with_audio = annotated

    composed = output_dir / "composed.mp4"
    if args.captions:
        style = "FontName=Inter,FontSize=22,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BackColour=&H80000000,Bold=1,Outline=2,Shadow=1,Alignment=2,MarginV=40"
        run_ffmpeg([
            "-i", str(with_audio), "-vf", f"subtitles={args.captions}:force_style='{style}'",
            "-c:a", "copy", str(composed),
        ])
    else:
        composed.write_bytes(Path(with_audio).read_bytes())

    print(json.dumps({"status": "ok", "composed": str(composed)}))


if __name__ == "__main__":
    main()
