---
name: visual-learner
description: Builds a complete, researched course on any subject and teaches it as a series of narrated explainer videos on a schedule. Use when someone wants to learn a topic in depth ("teach me X", "make me a course on X", "I want to learn X in 3 weeks", "daily lessons on X"). It interviews the learner (topic, lesson length, complexity, time frame and, for more than one video, what time the lessons should arrive), researches the subject thoroughly, writes a course book as a living doc, then schedules tasks that each turn the next chapter into an interactive narrated page and an MP4. Prefer quality and accuracy over lower usage costs throughout.
---

# Visual Learner

Turn "I want to learn X" into a researched course book plus a series of narrated, animated explainer videos that arrive on the learner's schedule. Each lesson ships three ways: a chapter in the course book (a living doc), an interactive page (a published Artifact with play, seek and scene controls), and an MP4 file.

This skill came out of a real 14-day course, "Investing & Finance in India 101", built for a 19-year-old beginner. The rules below are the ones that made that course work. Follow them unless the learner asks otherwise.

## Ground rules

- **Quality and knowledge first, cost second.** Use extended web search, open and read primary sources, verify every number, spawn a fresh-eyes reviewer for each chapter, and never shorten a lesson to save tokens. If something is costly but improves accuracy or understanding, do it.
- **Facts come from research, not memory.** Every rate, price, law, date and statistic in the book is looked up, read on the source page, cited, and dated "as of". Anything that can't be sourced is labelled approximate.
- **Pitch to the learner, not to an expert.** Define every new term in plain words the first time it appears, give a line of intuition or a tiny example built from the chapter's own numbers, and link back to the lesson where an earlier term was introduced.
- **Videos explain everything in their chapter.** Every section, table, worked example and new term appears on screen and in the narration. The video uses only the figures in the book.
- **Never fake it.** No invented quotes, reviews, people or sources. Worked examples use clearly made-up companies or people, and say so.

## Phase 1 — Intake (ask before any work)

Use the AskUserQuestion tool. The full question set, with options, is in `references/intake.md`. In short:

1. **Topic and goal**: the subject, why they want it, and what they already know.
2. **Lesson duration**: minutes per video (default about 10).
3. **Complexity**: always ask. Beginner (assumes nothing), Intermediate, Advanced, or Beginner-to-advanced.
4. **Time frame**: always ask "In what time frame do you want to finish the course?" (for example 1 week, 2 weeks, 1 month). Together with lesson length, this sets how many lessons there are and how many arrive per release.
5. **Delivery time**: if the course will produce **more than one video**, ask exactly: **"What time should the task run?"** Also confirm the time zone and the days (every day, weekdays only).
6. **Region and context** when the subject depends on it (currency, laws, tax, exams), plus the narrator voice (default Kokoro "af_heart").

If the session is unattended, pick sensible defaults, state them at the top of the work, and carry on.

## Phase 2 — Research

Follow `references/research.md`. Research comes before any outline is fixed: the shape of the course falls out of what the subject actually contains.

- Map the subject: core concepts, the order they depend on each other, the common misconceptions, and what a learner at this level must be able to *do* at the end.
- For anything current or regional, use the WebSearch tool in "extended" mode and fetch the source pages you take facts from. Keep a source list with URLs and an as-of date.
- Find the numbers worked examples will use, and check each one twice.
- Hand the draft outline to a subagent for review, with no conclusions attached: "What is missing, wrong or out of order for a <level> learner?"

## Phase 3 — Design the course

1. Count the lessons: `lessons = days in the time frame × lessons per release`. Keep each lesson to one sitting at the chosen length (about 150 spoken words a minute, so a 10-minute lesson is roughly 1,300–1,600 words of narration).
2. Group lessons into parts (foundations → core skills → applying it). The last lesson is always a set of scenario problems that combine everything, each posed, paused on, then solved step by step.
3. Write a release schedule: date → lesson numbers.
4. Show the outline and schedule to the learner and get a yes before writing the book (skip only when unattended).

## Phase 4 — Write the course book (a living doc)

Create the book with Claude Docs (load the docs skill first if it is listed): title, byline, a "How to use this book" section, then one section per lesson, then a glossary, a cheat sheet and sources. Plant the outline first, then fill it chapter by chapter. Chapter rules are in `references/chapter-style.md`: definitions in bold at first use, intuition lines, back-links ("Day 3"), worked examples step by step, a "New words in this chapter" list of about 10 terms, and a Practice checklist.

Add a **Release schedule** table to the book (date, lessons, status, video links) so every scheduled run can find its work and record what it shipped.

## Phase 5 — Publish the build kit

Scheduled runs start in fresh sessions with no memory of this one, so everything they need must live somewhere they can fetch it:

1. Copy `scripts/` (engine.py, template.html, common.py, lexicon.py, record.js, check.js) and `examples/day1.py` into a build folder.
2. Adapt `lexicon.py` to the course (acronyms, names and non-English words), and if the subject suits a different look, retheme the stage tokens in `template.html` once (the palette lives in its `:root` block; keep every lesson identical after that).
3. Publish a small "Build Kit" page with the Artifact tool that lists the files and the setup block from `references/video-production.md`, with the files attached through `files`. Record its URL; every scheduled prompt references it.

## Phase 6 — Schedule the lessons

Create the scheduled tasks with the `create_trigger` tool (load it with ToolSearch). Never use local cron tools: they die with the session. Details and the prompt template are in `references/scheduling.md`:

- One recurring task at the time the learner chose (`CRON_TZ=<their zone>`), or one-shot tasks per release when releases are irregular.
- The prompt is complete and standalone: course doc id and link, kit artifact link, learner profile, level, lesson length, the chapter rules, the video rules, and how to find today's lessons in the Release schedule table.
- After the last release, the task disables itself with `update_trigger` (enabled=false).
- Tell the learner which approval setting each task got and, if runs will ask for approval, that they can switch the task to "Automatically approve" in its settings.

Then produce Lesson 1 now, live, so the learner sees the format and can ask for changes before the schedule takes over.

## Phase 7 — Each lesson (what every run does)

Follow `references/video-production.md` and the checklist in `references/quality-checklist.md`:

1. Read the chapter in full from the book. If it isn't yet pitched at the learner's level, rewrite it in place first (keep every fact, figure, table and example; define, add intuition, back-link, add New words) with one doc update that inserts the new chapter and deletes the old blocks.
2. Write `dayN.py`: 16–21 scenes, warm conversational narration with numbers spelled out for speech, a short caption and a real animation per scene (counters, growing bars, tables revealed row by row, formulas worked step by step). End with a New words scene, then Practice. Scenario lessons add `hold` so each problem gets a 3-second "Pause and think" countdown before its answer.
3. `python3 engine.py dayN` → narration MP3 and page. Check the length; trim narration rather than exceed the agreed duration by more than about 10%.
4. `node check.js N` → look at the screenshots once, fix overlaps, rebuild.
5. Publish the page with the Artifact tool (icon "video", a one-sentence description).
6. `node record.js dayN.html mp4/dayN.mp4 v2outN/dayN.mp3` (at most two at once on a 2-core machine, after all audio is built). Confirm with ffprobe that the MP4 duration matches the MP3.
7. Send the MP4s with SendUserFile, update the Release schedule row (status, links), send a short SendUserMessage, and send a PushNotification with a `<routine_summary>`.

## What to tell the learner at the end of setup

One short message: the course book link, the number of lessons and parts, the release schedule (time and zone), the approval setting of the scheduled task, and that Lesson 1 is ready to watch.
