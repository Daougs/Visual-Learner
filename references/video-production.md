# Video production

## Setup (once per session)

```bash
mkdir -p ~/build/shots ~/build/mp4 ~/models
pip install --break-system-packages kokoro-onnx soundfile numpy
curl -sSL -o ~/models/kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
curl -sSL -o ~/models/voices-v1.0.bin   https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
cd ~/build && npm i playwright @fontsource-variable/bricolage-grotesque @fontsource/instrument-sans @fontsource/jetbrains-mono
# copy engine.py, template.html, common.py, lexicon.py, record.js, check.js (from the kit artifact or this skill's scripts/)
```

ffmpeg and ffprobe must be installed. If a preinstalled Chromium exists at `/opt/pw-browsers/chromium` the scripts use it; otherwise set `CHROME=/path/to/chrome` or run `npx playwright install chromium`. Set `KOKORO_DIR` if the models aren't in `~/models`.

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
python3 engine.py dayN            # prints scene sum, mp3 length (must match), words and length
node check.js N                   # script errors, 400px overflow, screenshots in shots/
node record.js dayN.html mp4/dayN.mp4 v2outN/dayN.mp3   # real time; at most two at once on 2 cores
ffprobe -v error -show_entries format=duration -of csv=p=0 mp4/dayN.mp4
```

- Look at the screenshots once (tile them into one image), fix overlaps and clipped text, rebuild (audio is cached per sentence, so rebuilds are fast), then publish.
- Blocked Google Fonts in check.js are expected and harmless; record.js loads the same faces from local @fontsource files.
- Publish each page as its own artifact: `<title>` is "Day N Explainer", icon "video", and a one-sentence description.
- Build all audio before recording, then record at most two MP4s at once.

## Voices

Default Kokoro voice `af_heart` at speed 0.95, sentence by sentence with 0.3 s gaps, 0.4 s lead-in and 1.5 s tail per scene. Set `VOICE` / `SPEED` in a lesson file to change them, but keep one voice for the whole course. Fix mispronounced names and non-English words in `lexicon.py` (IPA), and acronyms in `SPEECH`.
