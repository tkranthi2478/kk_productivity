---
name: yt-transcript
description: Download only the captions of any YouTube video (no video or audio) and write a clean, timestamped transcript with title, channel and chapters. Use when the user shares a YouTube link and asks what it says, wants a summary, transcript or notes, or asks whether we can do what the video shows. Not for adding videos to the Hello Interview library (use `hi`).
---

# yt-transcript: captions only

```bash
python3 -I <this-skill>/scripts/yt_transcript.py "<youtube-url>" --out-dir <scratchpad>
```

- Writes `<out-dir>/<video-id>/transcript.md`, plus the raw `.vtt` and `info.json`.
  Prints the title, channel, caption track and the transcript path.
- Default `--out-dir` is the current folder. Use the session scratchpad unless the
  user names a location.
- `--timestamps N` starts a `[m:ss]` paragraph roughly every N seconds (default 60,
  `0` = one block). `--lang CODE` picks another track, e.g. `en-GB` or `de`.
- Picks human-made English captions first, then `en-orig` (YouTube's speech
  recognition), then auto `en`. The header says which one was used. With
  auto-captions, names and terms are often mis-heard (e.g. "Entropic" for
  Anthropic), so correct them in summaries; never quote them as exact.
- It asks for exactly one language. A wildcard like `en.*` fetches dozens of
  translated tracks and triggers HTTP 429. The script retries a 429 with backoff.
- A plain web fetch of a YouTube page returns only navigation, so use this script
  instead.
- Requires `yt-dlp` on PATH (`brew install yt-dlp`). If YouTube still refuses after
  retries, report that; don't invent a summary from the title.

When summarising, read `transcript.md` and say that the summary comes from captions.
