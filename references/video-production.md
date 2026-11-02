# Video production

## Setup (once per session)

Every dependency is pinned to an exact version, and the voice model files are checked against fixed SHA-256 hashes before use.

```bash
mkdir -p ~/build/shots ~/build/mp4 ~/models
pip install --break-system-packages kokoro-onnx==0.6.1 soundfile==0.14.0 numpy
curl -sSL -o ~/models/kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
curl -sSL -o ~/models/voices-v1.0.bin   https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
cd ~/models && sha256sum -c - <<'SUMS'
7d5df8ecf7d4b1878015a32686053fd0eebe2bc377234608764cc0ef3636a6c5  kokoro-v1.0.onnx
bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d  voices-v1.0.bin
SUMS
cd ~/build && npm i playwright@1.50.1 @fontsource-variable/bricolage-grotesque@5.3.0 @fontsource/instrument-sans@5.3.0 @fontsource/jetbrains-mono@5.3.0
# copy engine.py, template.html, common.py, lexicon.py, record.js, check.js (from the kit artifact or this skill's scripts/)
```

If `sha256sum -c` reports a mismatch, stop and don't use the files. ffmpeg and ffprobe must be installed for recording. If a preinstalled Chromium exists at `/opt/pw-browsers/chromium` the scripts use it; otherwise pass `--chrome=/path/to/chrome` or run `npx playwright install chromium`. Pass `--models <folder>` to engine.py if the models aren't in `~/models`.

## The lesson file (`dayN.py`)

Module-level `DAY`, `H1`, `SUB`, `CSS`, `SCENES`. See `examples/day1.py` for every pattern.

Each scene is a dict:

| Key | What it is |
|---|---|
| `label` | Short name for the scene button ("Gold", "3 · Answer") |
| `cap` | On-screen caption, one or two short lines; ₹ and digits are fine |
| `show` | Note of what the visual shows (goes into the script file) |
| `say` | Narration. Numbers spelled for speech ("one point two five lakh rupees", "twelve point five percent"). Acronyms as written; `lexicon.py` respells them |
| `html` | The scene's markup, using the template's building blocks (`.big`, `.mid`, `.eq` + `.chip`, `.hbar`, `.bars`, `.tbl` via `common.table`, `.cards`/`.card`, `.split2`, `.vs`, `.sbar`, `.chips`, `.stamp`, `checks()`) and classes from `CSS` |
| `js` | Body of `render(t, D)`: `t` is seconds into the scene, `D` the spoken length. Reveal times are fractions of `D` (`show('x0', t > .3*D)`). Helpers: `show`, `seq`, `txt`, `w`, `h`, `P(t,a,b)` (eased 0→1), `inr(n)` (₹ with Indian grouping) |
| `hold` | Optional extra seconds of silence after the narration (use 1.6 for a 3-second pause-and-think) |

Rules:

- 16–21 scenes; about 1,300–1,700 words for a 10-minute lesson. Measure after the first build and trim narration if the length runs more than about 10% over.
- Open with a title scene, end with **New words** (the chapter's glossary on screen) and then **Practice** (`common.checks`).
- Define each new term in the narration the moment it appears, and add a sentence of intuition, why it matters, or a link back to an earlier day after each point.
- Animate the real content: counters that count to the answer, bars that grow to scale, tables revealing row by row, formulas computed step by step. Every element id is unique across the whole page (use a letter prefix per scene).
- Never use the browser's speechSynthesis; the narration is the embedded MP3.

## Build, check, publish, record

```bash
python3 engine.py dayN            # narration MP3 + page; prints scene sum, MP3 length (must match), words, length
node check.js N                   # script errors, 400px overflow, screenshots in shots/
node record.js dayN.html mp4/dayN.mp4 v2outN/dayN.mp3   # real time; at most two at once on 2 cores
ffprobe -v error -show_entries format=duration -of csv=p=0 mp4/dayN.mp4
```

- Look at the screenshots once (tile them into one image), fix overlaps and clipped text, rebuild (audio is cached per sentence, so rebuilds are fast), then publish.
- engine.py runs no external programs (audio is stitched and encoded in Python). record.js runs only ffprobe and ffmpeg, with fixed arguments and no shell.
- Blocked Google Fonts in check.js are expected and harmless; record.js loads the same faces from local @fontsource files.
- Publish each page as its own artifact: `<title>` is "Day N Explainer", icon "video", and a one-sentence description.
- Build all audio before recording, then record at most two MP4s at once.

## Voices

Default Kokoro voice `af_heart` at speed 0.95, sentence by sentence with 0.3 s gaps, 0.4 s lead-in and 1.5 s tail per scene. Set `VOICE` / `SPEED` in a lesson file to change them, but keep one voice for the whole course. Fix mispronounced names and non-English words in `lexicon.py` (IPA), and acronyms in `SPEECH`.
