# Chapter style

The course book is a Claude Docs living doc. One `## Day N: <title>` section per lesson, `###` subsections inside.

## Every chapter, at Beginner level

1. **Opening paragraph**: what this chapter is for and why it matters, linked to what came before ("On Day 6 you learned to read a company's numbers; today you use them to judge the price").
2. **Define every term at first use.** Bold the term, then a plain-English definition in the same sentence. Acronyms are spelled out once.
3. **Add intuition after each point.** One line: an everyday comparison, or a tiny example built only from numbers already in the chapter ("at 2–3%, every ₹100 of property earns ₹2–3 a year"). Arithmetic on the book's figures is fine; never introduce new market rates, prices or rules that weren't researched.
4. **Back-link earlier terms**: "(Day 3)" after a term taught earlier.
5. **Tables for comparisons, then "The words in that table"**: a bullet per term the table used.
6. **Worked examples step by step**: state the problem, then each line of arithmetic, then the takeaway.
7. **Common mistakes** where the subject has traps.
8. **`### New words in this chapter`**: about 10 terms, one line each, just before Practice.
9. **`### Practice`**: 2–3 checkbox tasks the learner can do with real data.

At Intermediate or Advanced level, keep 1, 4, 6 and 9; move definitions to the glossary and spend the room on depth.

## The final lesson: scenarios

8 or so cases plus a bonus that combine several earlier lessons. Each: a named person, the facts, a question, then "**Answer:**" with the reasoning and every step of the numbers. In the video, each case pauses for 3 seconds ("Pause and think") between the question and the answer.

## Rewriting a chapter in place (Claude Docs)

1. Read the doc's outline (`projection: "outline"`) to get the chapter's block ids and the `rev`. Export the tab as markdown to read the full text.
2. Write the new chapter in markdown, keeping every fact, figure, table, scenario and example.
3. One `update` call on the tab's body: an `insert` of the new markdown with `side: "before"` the old `## Day N` heading, then a `delete` of all the old chapter's top-level block ids with `ifRev` from the read. Touch no other chapter.
4. If you correct something the old text got wrong (its own numbers don't add up), keep the fix and mention it to the learner.
