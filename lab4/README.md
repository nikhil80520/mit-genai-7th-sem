# Lab 4 - Workflow Design with LLMs

Each script implements one lab exercise using the same Groq and `.env` setup as Lab 3. Every workflow keeps its stages separate: later prompts receive the structured output of the earlier stage, rather than the original raw input.

## Setup

Install the dependencies used in the earlier labs and add your key to the root `.env` file:

```text
GROQ_API_KEY=your_key_here
```

Run any exercise from the repository root, for example:

```powershell
python lab4/exercise1_candidate_outreach.py
```

## Exercises

1. `exercise1_candidate_outreach.py` - job posting to requirements and candidate outreach
2. `exercise2_news_fact_card.py` - article claims to fact card
3. `exercise3_meeting_action_items.py` - transcript to discussion, flagged actions, and task table
4. `exercise4_product_pitch.py` - product idea to structured and investor pitches
5. `exercise5_bug_fix_plan.py` - bug report to normalized report, gaps, and fix plan
6. `exercise6_recipe_grocery_list.py` - recipe ingredients to a scaled grocery list
