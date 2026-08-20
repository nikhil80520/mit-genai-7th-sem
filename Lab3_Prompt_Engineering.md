# Lab 3 — Prompt Engineering

## GitHub Repository Setup

Use the same repository from previous labs: `generative_ai_<student-name-or-roll-no>`. Push work for each exercise after completing it.

---

## Exercise 1 — Doctor Summary Generator

Build a prompt that takes a patient's raw consultation notes and generates a clean doctor's summary.

**Input:** `patient_notes`, `patient_name`

**Output:** a summary with fixed sections — Symptoms, Diagnosis, Recommendation — in the same format every time, regardless of input

**Upload to GitHub.**

---

## Exercise 2 — Review Classifier

Build a prompt that takes a customer review and returns a category label.

**Input:** `review_text`

**Output:** a single category label (categories, rules, and definitions are for you to decide)

**Upload to GitHub.**

---

## Exercise 3 — Resume Field Extractor

Build a prompt that takes resume text and pulls out only the requested fields.

**Input:** `resume_text`, `fields_to_extract`

**Output:** strict JSON containing only the requested fields, nothing else

**Upload to GitHub.**

---

## Exercise 4 — Customer Support Reply Generator

Build a prompt that generates a support reply to a customer message.

**Input:** `customer_message`, `company_name`, `max_words`

**Output:** a reply that stays within the word limit, with consistent tone across different inputs

**Upload to GitHub.**

---

## Exercise 5 — Multi-language Translator

Build a prompt that translates a sentence into a target language at a given formality level.

**Input:** `sentence`, `target_language`, `formality`

**Output:** a translated sentence matching the requested formality level

**Upload to GitHub.**

---

## Exercise 6 — Iterative Content Refiner

Build a prompt that takes a draft and revises it to fix one specific issue, across multiple rounds.

**Input:** `draft_text`, `issue_to_fix`

**Output:** a revised version of the text that resolves that specific issue, run for at least 3 rounds

**Upload to GitHub.**

---

## Final Submission

Push all exercise work to `generative_ai_<student-name-or-roll-no>` and share the repository link:

```text
https://github.com/<username>/generative_ai_<student-name-or-roll-no>
```
