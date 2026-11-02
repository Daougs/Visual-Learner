# Scheduling the lessons

Use the remote scheduled-task tools (`create_trigger`, `update_trigger`, `list_triggers`, `delete_trigger`; load them with ToolSearch). Never use local cron tools: they live inside one session and silently stop.

## Choosing the shape

- **Regular releases** (every day, weekdays): one recurring task. `cron_expression` in the learner's zone, e.g. `CRON_TZ=Asia/Kolkata 0 7 * * *` for 7:00 am daily. If the learner picked a time on the hour or half hour, you may move it a few minutes earlier to avoid the busiest minute, and tell them.
- **Irregular releases**: one task per release with `run_once_at`.
- Check `list_triggers` first so you don't duplicate an existing course task.
- `initiation`: `human_request`. Leave `permission_mode` unset, then tell the learner which setting the task got. If its runs will ask for approval, say they can turn on "Automatically approve" in the task's settings, if their organization allows it.
- Set `notifications` to `{"push": true}`, plus email only if the learner asked for email.

## The prompt

Each run starts a fresh session with no memory, so the prompt must stand alone. Template:

```
Make today's narrated explainer video(s) for <learner name>'s course "<course title>".
Learner: <age/background>, <level> level, <region>. Lesson length: about <N> minutes. Work unattended; don't ask questions.

SOURCE: the course book is a Claude Docs doc, id <doc id> (<doc link>). Load the Claude Docs tools via ToolSearch and call its guide with ["topic.index", "topic.editing"] once. Read the "Release schedule" table: today's lessons are the first row whose Status is not "Done". If every row is Done, disable this scheduled task with update_trigger (enabled=false) and send one notification that the course is complete.

STEP 0 — CHAPTER: read each of today's chapters in full. If it isn't yet pitched at <level> level (rules: <paste the chapter-style rules>), rewrite it in place with one Claude Docs update per chapter (insert new markdown before its "## Day N" heading and delete the old chapter's top-level blocks, ids and ifRev from an outline read). Touch no other chapter. Re-check any fast-moving figure with one extended web search; if it changed, update the book and note it.

BUILD KIT: read the kit artifact <kit link> with the Artifact tool (action "read"), fetch its files (paths ["engine.py","template.html","common.py","lexicon.py","record.js","check.js","day1.py"]) into ~/build, and follow its setup block. Load the artifact-design skill before writing pages.

VIDEO: write ~/build/dayN.py (format of day1.py): 16–21 scenes, about <words> spoken words, warm and plain for this learner, every term defined as it appears, every section/table/worked example/new word of the chapter covered, figures only from the book, a New words scene then Practice. Scenario lessons: hold=1.6 on each question scene for a 3-second "Pause and think". Run python3 engine.py dayN; node check.js N once and fix overlaps; confirm MP3 length = scene sum; publish the page with the Artifact tool (icon "video", one-sentence description); record with node record.js (at most two at once, after all audio is built); check each MP4 with ffprobe; send the MP4s with SendUserFile (status "proactive").

FINISH: set today's Release schedule row to Done with the page links; send a short SendUserMessage listing the videos; send a PushNotification with a <routine_summary> (the first sentence names the lessons). If anything failed, notify with what failed and what was still delivered.
```

## After the last lesson

The final run disables the task. Offer the learner a review run (a week later) that re-tests them on the scenarios.
