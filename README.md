# Visual Learner — a Claude skill

Tell Claude what you want to learn. It interviews you, researches the subject properly, writes you a course book, and then teaches it to you as a series of narrated, animated explainer videos that arrive on your schedule.

Built and tested on a real 14-day course, **Investing & Finance in India 101**, taught to a complete beginner.

## What you get

For every lesson:

- **A chapter** in a living course book (Claude Docs), written for your level: every term defined at first use, worked examples step by step, a "New words" list and practice tasks.
- **An interactive video page** (a published Claude Artifact): animated scenes driven by the narration, captions, play/pause, seek bar with scene ticks, scene buttons, voiceover toggle, keyboard and reduced-motion support.
- **An MP4** (1280×720, H.264 + AAC) you can watch anywhere.

Lessons are produced by scheduled tasks at the time you choose, so a new one is waiting for you each day.

## How it works

1. **Intake.** Claude asks for the topic, video length, complexity (beginner → advanced), the time frame to finish the course, and — if there's more than one video — *"What time should the task run?"*
2. **Research.** Extended web search, primary sources opened and cited, numbers computed in code and checked twice, and a fresh-eyes review of the outline. Quality is prioritised over lower usage costs.
3. **Design.** Lessons are counted from your time frame and pace, grouped into parts, and end with a scenario lesson that pauses on each problem before solving it.
4. **Book.** The full course is written as a living doc with a release schedule.
5. **Schedule.** One scheduled task delivers each release; Lesson 1 is built live so you can see the format first.
6. **Each lesson.** Chapter check → script → narration (Kokoro TTS, offline) → animated page → screenshot check → publish → MP4 → notification.

## Install

**Claude apps (claude.ai / desktop):** download `visual-learner.zip` from the Releases page and upload it where your plan lets you add skills (Settings → Capabilities → Skills, if your organization allows custom skills).

**Claude Code:** copy the folder into your skills directory:

```bash
git clone https://github.com/<your-username>/visual-learner.git
cp -r visual-learner ~/.claude/skills/
```

Then ask: *"Make me a course on <topic>."*

## Requirements for video builds

Python 3 with `kokoro-onnx`, `soundfile`, `numpy`; ffmpeg/ffprobe; Node.js with Playwright and Chromium. The setup block is in `references/video-production.md`. Scheduling needs Claude's scheduled tasks; the course book uses Claude Docs.

## Repository layout

```
SKILL.md                     the skill: phases and rules Claude follows
references/
  intake.md                  the questions Claude asks, with defaults
  research.md                research protocol (sources, verification, review)
  chapter-style.md           how chapters are written and rewritten
  video-production.md        lesson file format, build/check/record commands
  scheduling.md              scheduled-task setup and the standalone run prompt
  quality-checklist.md       per-lesson checklist
scripts/
  engine.py                  narration (Kokoro) + page builder
  template.html              the animated player page
  common.py                  table and practice helpers
  lexicon.py                 pronunciation fixes (acronyms, names, non-English words)
  check.js                   page check: errors, 400px overflow, screenshots
  record.js                  records a page to MP4 with the narration
examples/
  day1.py                    a short lesson showing every scene pattern
```

## License

MIT — see `LICENSE`.
