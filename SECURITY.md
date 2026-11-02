# Security notes

Automated scanners flag some patterns in this skill. Here is exactly what each script does, so you can judge for yourself.

| File | What it does | What it does not do |
|---|---|---|
| `scripts/engine.py` | Reads a lesson file, synthesizes speech locally with Kokoro (an offline ONNX model), writes WAV/MP3 files and one HTML page into the current folder. | Runs no external programs, makes no network requests, reads no environment variables or secrets. |
| `scripts/check.js` | Opens the built page in a local headless browser, collects console errors, saves screenshots to `shots/`. | Runs no external programs, makes no network requests of its own, reads no environment variables. |
| `scripts/record.js` | Records the local page with a headless browser, then runs **ffprobe** (to measure the recording) and **ffmpeg** (to encode it with the narration) via `execFileSync` with fixed arguments and no shell. | Runs nothing else, makes no network requests of its own, reads no environment variables. |
| `scripts/common.py`, `lexicon.py`, `template.html` | Static helpers and the page template. | — |

Setup (in `references/video-production.md`) installs packages pinned to exact versions and verifies the downloaded voice-model files against fixed SHA-256 hashes. Run it in a sandbox or virtual environment if you prefer.

The page template loads fonts from Google Fonts; nothing else is fetched at view time.

Found a problem? Open an issue.
