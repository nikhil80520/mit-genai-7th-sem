# Lab 4 — Workflow Design with LLMs

## GitHub Repository Setup

Use the same repository from previous labs: `generative_ai_<student-name-or-roll-no>`. Push work for each exercise after completing it.

---

## Exercise 1 — Job Posting to Candidate Outreach Pipeline

Build a 2-step pipeline. Step 1 extracts the key requirements from a raw job posting into structured form. Step 2 generates a personalized outreach message for a specific candidate, using the structured requirements from Step 1, not the raw posting.

**Input:** `job_posting_text`, `candidate_profile`

**Output:** the structured requirements from Step 1, and the personalized outreach message from Step 2

**Upload to GitHub.**

---

## Exercise 2 — News Article to Fact Card Pipeline

Build a 2-step pipeline. Step 1 extracts the core claims from a news article as a list. Step 2 generates a short "fact card" (headline, 3 bullet points, source confidence note) using only the extracted claims from Step 1.

**Input:** `article_text`

**Output:** the list of extracted claims from Step 1, and the fact card from Step 2

**Upload to GitHub.**

---

## Exercise 3 — Meeting Transcript to Action Items Pipeline

Build a 3-step pipeline. Step 1 extracts what was discussed from a raw meeting transcript. Step 2 identifies action items from that discussion, flagging anything where an owner or deadline is missing. Step 3 formats the final list into a structured task table.

**Input:** `transcript_text`

**Output:** the discussion summary from Step 1, the flagged action items from Step 2, and the final structured task table from Step 3

**Upload to GitHub.**

---

## Exercise 4 — Product Idea to Pitch Pipeline

Build a 2-step pipeline. Step 1 expands a one-line product idea into a structured pitch (problem, solution, target user). Step 2 generates a short investor-style pitch paragraph using only the structured version from Step 1, not the original one-liner.

**Input:** `product_idea`

**Output:** the structured pitch from Step 1, and the pitch paragraph from Step 2

**Upload to GitHub.**

---

## Exercise 5 — Bug Report to Fix Plan Pipeline

Build a 3-step pipeline. Step 1 normalizes a messy bug report into a structured format (steps to reproduce, expected vs actual behavior, severity). Step 2 checks the structured report for missing information and flags gaps. Step 3 generates a prioritized fix plan for a dev team based on the structured, gap-checked version.

**Input:** `bug_report_text`

**Output:** the structured report from Step 1, the flagged gaps from Step 2, and the fix plan from Step 3

**Upload to GitHub.**

---

## Exercise 6 — Recipe to Grocery List Pipeline

Build a 2-step pipeline. Step 1 extracts ingredients with quantities from a free-form recipe. Step 2 generates a consolidated grocery list scaled to a given number of servings, using only the extracted ingredients from Step 1.

**Input:** `recipe_text`, `target_servings`

**Output:** the extracted ingredient list from Step 1, and the scaled grocery list from Step 2

**Upload to GitHub.**

---

## Final Submission

Push all exercise work to `generative_ai_<student-name-or-roll-no>` and share the repository link:

```text
https://github.com/<username>/generative_ai_<student-name-or-roll-no>
```
