# Lab 5 — Workflow Design with LLMs (Prompt Templates & Output Parsers)

## GitHub Repository Setup

Use the same repository from previous labs: `generative_ai_<student-name-or-roll-no>`. Push work for each exercise after completing it.

For every exercise, build each step using `PromptTemplate` or `ChatPromptTemplate` and the output parser specified for that step, so each step's parsed output can be passed cleanly into the next step's prompt.

**General rule used throughout this lab:**
- Steps that **extract structured data** from messy/raw text → `PromptTemplate` + `PydanticOutputParser` (no persona needed, just schema + type-safe extraction)
- Steps that **generate free-form text** (a message, report, paragraph) → `ChatPromptTemplate` with a system persona + `StrOutputParser`
- Steps that **evaluate/flag issues or produce a final structured deliverable** → `ChatPromptTemplate` with a system persona + `PydanticOutputParser`

---

## Exercise 1 — Customer Review to Support Ticket Pipeline

Build a 2-step pipeline. Step 1 extracts the core complaint, product/feature mentioned, and customer sentiment from a raw customer review as structured data. Step 2 generates a support ticket summary for the internal team, using only the structured data from Step 1, not the raw review text.

**Input:** `review_text`

**Output:** the structured complaint data from Step 1, and the support ticket summary from Step 2

**Step 1 — Template:** `PromptTemplate` &nbsp;|&nbsp; **Parser:** `PydanticOutputParser` (fields: `complaint`, `product_or_feature`, `sentiment`)

**Step 2 — Template:** `ChatPromptTemplate` (system persona: "support ticket writer") &nbsp;|&nbsp; **Parser:** `StrOutputParser`

**Upload to GitHub.**

---

## Exercise 2 — Research Paper Abstract to Layperson Summary Pipeline

Build a 2-step pipeline. Step 1 extracts the research question, method, and key finding from a paper abstract as structured data. Step 2 generates a plain-language summary for a non-expert audience, using only the structured version from Step 1, not the original abstract.

**Input:** `abstract_text`

**Output:** the structured extraction from Step 1, and the layperson summary from Step 2

**Step 1 — Template:** `PromptTemplate` &nbsp;|&nbsp; **Parser:** `PydanticOutputParser` (fields: `research_question`, `method`, `key_finding`)

**Step 2 — Template:** `ChatPromptTemplate` (system persona: "science communicator explaining to a general audience") &nbsp;|&nbsp; **Parser:** `StrOutputParser`

**Upload to GitHub.**

---

## Exercise 3 — Interview Transcript to Candidate Scorecard Pipeline

Build a 3-step pipeline. Step 1 extracts the candidate's answers to each interview question from a raw transcript. Step 2 evaluates each answer against a given set of skills, flagging any skill that wasn't clearly demonstrated. Step 3 formats the evaluation into a structured hiring scorecard with an overall recommendation.

**Input:** `transcript_text`, `skills_to_assess`

**Output:** the extracted answers from Step 1, the flagged skill evaluation from Step 2, and the final scorecard from Step 3

**Step 1 — Template:** `PromptTemplate` &nbsp;|&nbsp; **Parser:** `PydanticOutputParser` (field: list of `question` + `answer` pairs)

**Step 2 — Template:** `ChatPromptTemplate` (system persona: "technical interviewer evaluating skill evidence") &nbsp;|&nbsp; **Parser:** `PydanticOutputParser` (fields: `skill`, `demonstrated: bool`, `evidence_or_gap`)

**Step 3 — Template:** `ChatPromptTemplate` (system persona: "hiring panel coordinator") &nbsp;|&nbsp; **Parser:** `PydanticOutputParser` (fields: list of scorecard rows + `overall_recommendation`)

**Upload to GitHub.**

---

## Exercise 4 — Travel Preferences to Itinerary Pitch Pipeline

Build a 2-step pipeline. Step 1 expands a short travel preference statement into a structured trip profile (destination type, budget level, trip duration, interests). Step 2 generates a short, persuasive itinerary pitch aimed at the traveler, using only the structured profile from Step 1, not the original preference statement.

**Input:** `travel_preference_text`

**Output:** the structured trip profile from Step 1, and the itinerary pitch from Step 2

**Step 1 — Template:** `PromptTemplate` &nbsp;|&nbsp; **Parser:** `PydanticOutputParser` (fields: `destination_type`, `budget_level`, `trip_duration`, `interests`)

**Step 2 — Template:** `ChatPromptTemplate` (system persona: "enthusiastic travel agent") &nbsp;|&nbsp; **Parser:** `StrOutputParser`

**Upload to GitHub.**

---

## Exercise 5 — Customer Support Chat Log to Escalation Report Pipeline

Build a 3-step pipeline. Step 1 normalizes a messy support chat log into a structured summary (issue, customer tone, resolution attempted). Step 2 checks the structured summary for missing information needed to escalate the issue (e.g. account ID, error code) and flags any gaps. Step 3 generates a prioritized escalation report for the support lead based on the structured, gap-checked version.

**Input:** `chat_log_text`

**Output:** the structured summary from Step 1, the flagged gaps from Step 2, and the escalation report from Step 3

**Step 1 — Template:** `PromptTemplate` &nbsp;|&nbsp; **Parser:** `PydanticOutputParser` (fields: `issue`, `customer_tone`, `resolution_attempted`)

**Step 2 — Template:** `ChatPromptTemplate` (system persona: "escalation-readiness reviewer") &nbsp;|&nbsp; **Parser:** `PydanticOutputParser` (fields: `missing_fields: list`, `is_ready_to_escalate: bool`)

**Step 3 — Template:** `ChatPromptTemplate` (system persona: "support operations lead") &nbsp;|&nbsp; **Parser:** `StrOutputParser`

**Upload to GitHub.**

---

## Exercise 6 — Workout Goal to Weekly Plan Pipeline

Build a 2-step pipeline. Step 1 extracts fitness goal details (goal type, current fitness level, days available per week, equipment access) from a free-form fitness goal description. Step 2 generates a structured weekly workout plan scaled to the extracted availability, using only the extracted details from Step 1, not the original description.

**Input:** `fitness_goal_text`, `days_per_week`

**Output:** the extracted goal details from Step 1, and the weekly workout plan from Step 2

**Step 1 — Template:** `PromptTemplate` &nbsp;|&nbsp; **Parser:** `PydanticOutputParser` (fields: `goal_type`, `fitness_level`, `days_available`, `equipment_access`)

**Step 2 — Template:** `ChatPromptTemplate` (system persona: "certified personal trainer") &nbsp;|&nbsp; **Parser:** `PydanticOutputParser` (field: list of day-by-day plan entries)

**Upload to GitHub.**

---

## Final Submission

Push all exercise work to `generative_ai_<student-name-or-roll-no>` and share the repository link:

```text
https://github.com/<username>/generative_ai_<student-name-or-roll-no>
```
