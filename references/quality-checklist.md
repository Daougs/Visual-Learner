# Quality checklist (run for every lesson)

## Content
- [ ] Every fact, rate and rule in the chapter traces to a source in the book's Sources list, with an as-of date, or is marked approximate.
- [ ] Every worked example was computed in code, and its numbers match the book exactly.
- [ ] Every new term is bold and defined at first use; earlier terms link back to their day.
- [ ] The chapter ends with New words (about 10) and Practice.
- [ ] A fresh-eyes subagent read the chapter for errors and gaps (give it the text, not your opinion of it).

## Video
- [ ] Every subsection, table, worked example and new word of the chapter appears in the video.
- [ ] No figure appears in the video that isn't in the book.
- [ ] Narration spells numbers for speech; acronyms and names are in `lexicon.py` and sound right.
- [ ] Length is within about 10% of the agreed duration; the MP3 length equals the scene-duration sum.
- [ ] `check.js`: no script errors except blocked Google Fonts, no horizontal scroll at 400 px.
- [ ] Screenshots looked at once; no overlaps, clipped text or unreadable contrast.
- [ ] MP4 is 1280×720, 30 fps, H.264 + AAC, and its duration matches the MP3.

## Delivery
- [ ] Page published (title "Day N Explainer", icon "video", one-sentence description).
- [ ] MP4s sent with SendUserFile.
- [ ] Release schedule row updated with status and links.
- [ ] Learner notified (PushNotification with a routine summary) — including when something failed.
