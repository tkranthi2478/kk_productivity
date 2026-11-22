#!/usr/bin/env python3
"""Download only the captions of a YouTube video and write a clean transcript.

Usage: yt_transcript.py <url> [--out-dir DIR] [--lang CODE] [--timestamps SECONDS]

Writes <out-dir>/<video-id>/:
  info.json        yt-dlp metadata (no media)
  <id>.<lang>.vtt  the raw caption file
  transcript.md    header (title, channel, duration, caption source), chapters, text

No video or audio is downloaded. Exits non-zero, saying why, when no English
captions exist or YouTube keeps refusing.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

RETRIES = 4


def run_ytdlp(args: list[str]) -> subprocess.CompletedProcess:
    """Run yt-dlp, retrying with backoff when YouTube rate-limits (HTTP 429)."""
    for attempt in range(RETRIES):
        proc = subprocess.run(["yt-dlp", *args], capture_output=True, text=True)
        if "429" not in proc.stderr:
            return proc
        wait = 15 * (attempt + 1)
        print(f"YouTube rate-limited the request; retrying in {wait}s", file=sys.stderr)
        time.sleep(wait)
    return proc


def pick_track(info: dict, lang: str | None) -> tuple[str, str]:
    """Return (language key, 'manual' | 'auto'), preferring human-made captions."""
    manual = {k: v for k, v in (info.get("subtitles") or {}).items() if k != "live_chat"}
    auto = info.get("automatic_captions") or {}
    if lang:
        if lang in manual:
            return lang, "manual"
        if lang in auto:
            return lang, "auto"
        sys.exit(f"No '{lang}' captions. Manual: {sorted(manual)}; auto: {len(auto)} languages")
    for key in sorted(manual):
        if key == "en" or key.startswith("en-"):
            return key, "manual"
    # en-orig is YouTube's speech recognition in the original language;
    # plain 'en' may be a machine translation when the video is not in English.
    for key in ("en-orig", "en"):
        if key in auto:
            return key, "auto"
    sys.exit(f"No English captions. Manual: {sorted(manual) or 'none'}; "
             f"auto: {sorted(auto)[:10] or 'none'}. Retry with --lang <code>.")


def parse_vtt(text: str) -> list[tuple[float, str]]:
    """Return (start seconds, line) pairs with tags and rolling duplicates removed."""
    out: list[tuple[float, str]] = []
    seen_recent: list[str] = []
    start = 0.0
    for block in re.split(r"\n\s*\n", text):
        lines = block.strip().splitlines()
        for i, line in enumerate(lines):
            m = re.match(r"(\d+):(\d{2}):(\d{2})\.(\d{3})\s+-->", line)
            if m:
                h, mi, s, ms = map(int, m.groups())
                start = h * 3600 + mi * 60 + s + ms / 1000
                for raw in lines[i + 1:]:
                    clean = re.sub(r"<[^>]+>", "", raw)
                    clean = clean.replace("&amp;", "&").replace("&gt;", ">").replace("&lt;", "<")
                    clean = clean.replace("&nbsp;", " ").strip()
                    # Auto captions repeat each line in the next cue; keep first sighting.
                    if clean and clean not in seen_recent:
                        out.append((start, clean))
                        seen_recent = (seen_recent + [clean])[-4:]
                break
    return out


def stamp(seconds: float) -> str:
    s = int(seconds)
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}" if s >= 3600 else f"{s // 60}:{s % 60:02d}"


def build_paragraphs(cues: list[tuple[float, str]], every: int) -> list[str]:
    """Group cue lines into paragraphs of roughly `every` seconds; 0 = one block."""
    if every <= 0:
        return [" ".join(line for _, line in cues)]
    paras, current, para_start = [], [], None
    for start, line in cues:
        if para_start is None:
            para_start = start
        current.append(line)
        if start - para_start >= every and line.rstrip().endswith((".", "?", "!")):
            paras.append(f"[{stamp(para_start)}] " + " ".join(current))
            current, para_start = [], None
    if current:
        paras.append(f"[{stamp(para_start or 0)}] " + " ".join(current))
    return paras


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--out-dir", default=".", help="parent folder; a <video-id>/ folder is made inside")
    ap.add_argument("--lang", help="caption language key, e.g. en, en-GB, de (default: best English)")
    ap.add_argument("--timestamps", type=int, default=60,
                    help="start a timestamped paragraph about every N seconds (0 = one block)")
    a = ap.parse_args()

    proc = run_ytdlp(["-J", "--no-warnings", "--ignore-no-formats-error", a.url])
    if proc.returncode != 0 or not proc.stdout.strip():
        sys.exit(f"Could not read video metadata:\n{proc.stderr.strip()}")
    info = json.loads(proc.stdout)
    vid = info["id"]
    folder = Path(a.out_dir).expanduser() / vid
    folder.mkdir(parents=True, exist_ok=True)
    info_path = folder / "info.json"
    info_path.write_text(json.dumps(info))

    lang, kind = pick_track(info, a.lang)
    # Ask for exactly one language: requesting en.* fetches dozens of
    # translated tracks and is what triggers HTTP 429.
    proc = run_ytdlp([
        "--load-info-json", str(info_path), "--skip-download", "--ignore-no-formats-error",
        "--write-subs" if kind == "manual" else "--write-auto-subs",
        "--sub-langs", lang, "--sub-format", "vtt/best", "--convert-subs", "vtt",
        "-o", str(folder / "%(id)s.%(ext)s"),
    ])
    vtts = sorted(folder.glob(f"{vid}.*.vtt"))
    if not vtts:
        sys.exit(f"Caption download failed:\n{proc.stderr.strip()}")
    cues = parse_vtt(vtts[0].read_text(encoding="utf-8", errors="replace"))
    if not cues:
        sys.exit(f"Caption file {vtts[0]} contained no text")

    source = "human-made captions" if kind == "manual" else "YouTube auto-captions (speech recognition; expect mis-heard names)"
    md = [f"# {info.get('title', vid)}", "",
          f"- Channel: {info.get('channel') or info.get('uploader', '?')}",
          f"- URL: {info.get('webpage_url', a.url)}",
          f"- Duration: {info.get('duration_string', '?')}",
          f"- Published: {info.get('upload_date', '?')}",
          f"- Captions: `{lang}`, {source}", ""]
    if info.get("chapters"):
        md += ["## Chapters", ""]
        md += [f"- {stamp(c['start_time'])} {c['title']}" for c in info["chapters"]]
        md.append("")
    md += ["## Transcript", ""]
    md += [p + "\n" for p in build_paragraphs(cues, a.timestamps)]
    out = folder / "transcript.md"
    out.write_text("\n".join(md), encoding="utf-8")

    words = sum(len(line.split()) for _, line in cues)
    print(f"{info.get('title')} | {info.get('channel')} | {info.get('duration_string')}")
    print(f"captions: {lang} ({kind}), {words} words")
    print(out.resolve())


if __name__ == "__main__":
    main()
