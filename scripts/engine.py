"""Build one narrated lesson page: Kokoro TTS per sentence -> one MP3 -> self-contained HTML.

Usage (from the build folder that holds this script, template.html, lexicon.py and dayN.py):
    python3 engine.py day3 [--models ~/models]

A lesson module defines DAY, H1, SUB, CSS and SCENES. Each scene is a dict with
label, cap, show, say, html, js (the body of render(t, D)), and optional hold
(extra seconds of silence after the narration, e.g. for "pause and think").
Optional module-level VOICE and SPEED override the defaults below.
"""
import argparse, base64, hashlib, importlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lexicon import SPEECH, IPA  # noqa: E402  (course-specific respellings and pronunciations)

MODELS = os.path.expanduser('~/models')  # override with --models
LEAD, TAIL, GAP = 0.4, 1.5, 0.3          # seconds before, after each scene; between sentences
VOICE, SPEED = 'af_heart', 0.95


def speechify(s):
    for a, b in SPEECH:
        s = re.sub(a, b, s)
    return s


def mp3_seconds(path):
    import soundfile as sf
    return sf.info(path).duration


_IPAT = re.compile(r"\b(" + '|'.join(sorted(map(re.escape, IPA), key=len, reverse=True)) + r")\b('s)?") if IPA else None


def to_phonemes(k, text):
    """Phonemize with espeak, but splice in fixed IPA for words in the lexicon (names, non-English terms)."""
    if not _IPAT:
        return k.tokenizer.phonemize(text, 'en-us')
    out, pos = [], 0
    for m in _IPAT.finditer(text):
        if m.start() > pos:
            out.append(k.tokenizer.phonemize(text[pos:m.start()], 'en-us'))
        out.append(IPA[m.group(1)] + ('z' if m.group(2) else ''))
        pos = m.end()
    if pos < len(text):
        out.append(k.tokenizer.phonemize(text[pos:], 'en-us'))
    return re.sub(r'\s+', ' ', ' '.join(o.strip() for o in out)).strip()


def sentences(text):
    return [x for x in re.split(r'(?<=[.!?])\s+', text.strip()) if x]


def make_audio(day, scenes, outdir, voice, speed, models):
    """Synthesize sentence by sentence and stitch everything in memory: no external programs are run."""
    import numpy as np, soundfile as sf
    from kokoro_onnx import Kokoro
    k = Kokoro(os.path.join(models, 'kokoro-v1.0.onnx'), os.path.join(models, 'voices-v1.0.bin'))
    cache = os.path.join(outdir, 'cache')
    os.makedirs(cache, exist_ok=True)
    SR = 24000

    def synth(sent):
        key = hashlib.sha1(f'v2|{voice}|{speed}|{sent}'.encode()).hexdigest()[:16]
        p = os.path.join(cache, key + '.wav')
        if not os.path.exists(p):
            a, sr = k.create(to_phonemes(k, speechify(sent)), voice=voice, speed=speed, is_phonemes=True)
            sf.write(p, a, sr)
        a, sr = sf.read(p, dtype='float32')
        assert sr == SR, sr
        return a

    clips, durs, reveals = [], [], []
    for i, sc in enumerate(scenes):
        parts = []
        sents = sentences(sc['say'])
        for j, sent in enumerate(sents):
            parts.append(synth(sent))
            if j < len(sents) - 1:
                parts.append(np.zeros(int(GAP * SR), dtype='float32'))
        audio = np.concatenate(parts)
        alen = len(audio) / SR
        dur = round(LEAD + alen + TAIL + sc.get('hold', 0), 2)
        clip = np.zeros(int(round(dur * SR)), dtype='float32')
        start = int(LEAD * SR)
        clip[start:start + len(audio)] = audio[:len(clip) - start]
        clips.append(clip); durs.append(dur); reveals.append(round(LEAD + alen, 2))
        print(f'  scene {i + 1}: audio {alen:.2f}s -> {dur:.2f}s', flush=True)
    mp3 = os.path.join(outdir, f'day{day}.mp3')
    sf.write(mp3, np.concatenate(clips), SR, format='MP3', subtype='MPEG_LAYER_III')
    return mp3, durs, reveals


def build(d, models=MODELS):
    root = os.getcwd()
    outdir = os.path.join(root, f'v2out{d.DAY}')
    os.makedirs(outdir, exist_ok=True)
    mp3, durs, reveals = make_audio(d.DAY, d.SCENES, outdir, getattr(d, 'VOICE', VOICE), getattr(d, 'SPEED', SPEED), models)
    total, mlen = sum(durs), mp3_seconds(mp3)
    words = sum(len(s['say'].split()) for s in d.SCENES)
    print(f'Day {d.DAY}: scene sum {total:.2f}s, mp3 {mlen:.2f}s, diff {mlen - total:+.3f}s, words {words}, '
          f'length {int(total // 60)}:{int(total % 60):02d}')
    template = open(os.path.join(HERE, 'template.html')).read()
    scenes_html = '\n'.join(
        f'<section class="scene{" on" if i == 0 else ""}" data-i="{i}" aria-hidden="{"false" if i == 0 else "true"}">{s["html"]}</section>'
        for i, s in enumerate(d.SCENES))
    scene_js = ',\n'.join(
        '{d:%s,r:%s,label:%s,cap:%s,render:(t,D)=>{%s}}' % (dur, rv, json.dumps(s['label']), json.dumps(s['cap']), s.get('js', ''))
        for s, dur, rv in zip(d.SCENES, durs, reveals))
    html = (template.replace('%%DAY%%', str(d.DAY)).replace('%%H1%%', d.H1).replace('%%SUB%%', d.SUB)
            .replace('/*%%CSS%%*/', d.CSS).replace('%%SCENES%%', scenes_html)
            .replace('/*%%SCENEJS%%*/', scene_js)
            .replace('%%AUDIO%%', base64.b64encode(open(mp3, 'rb').read()).decode()))
    out = os.path.join(root, f'day{d.DAY}.html')
    open(out, 'w').write(html)
    with open(os.path.join(outdir, 'script.txt'), 'w') as f:
        for i, (s, dur) in enumerate(zip(d.SCENES, durs)):
            f.write(f"Scene {i + 1} [{s['label']}] {dur}s\nCAPTION: {s['cap']}\nSHOW: {s.get('show', '')}\nSAY: {s['say']}\n\n")
    print('wrote', out, os.path.getsize(out), 'bytes')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Build one narrated lesson page.')
    ap.add_argument('lesson', help='lesson module name in the current folder, e.g. day3')
    ap.add_argument('--models', default=MODELS, help='folder holding kokoro-v1.0.onnx and voices-v1.0.bin')
    args = ap.parse_args()
    sys.path.insert(0, os.getcwd())
    build(importlib.import_module(args.lesson), args.models)
