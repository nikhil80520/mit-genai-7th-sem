"""Exercise 5: Normalize a bug report, flag gaps, and propose a fix plan."""
import json
import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY is missing from .env")
client = Groq(api_key=api_key)
MODEL = "openai/gpt-oss-20b"

NORMALIZE_PROMPT = """Normalize a bug report. Return valid JSON only with exactly these
keys: title, steps_to_reproduce, expected_behavior, actual_behavior, severity,
environment. Use null for unreported scalar values and [] for absent steps.
Severity must be critical, high, medium, low, or unknown. Do not infer facts."""
GAPS_PROMPT = """Check the structured bug report for missing or unclear information.
Return valid JSON only: {"gaps": ["specific missing or unclear item", ...]}.
Use only the report; an empty list means no gaps found."""
PLAN_PROMPT = """Create a prioritized development fix plan from the structured bug
report and its gap check only. Return a Markdown numbered list. Each item must
state priority, action, and any necessary validation. Distinguish investigation
needed for reported gaps; do not invent root causes."""


def ask_json(prompt, content):
    response = client.chat.completions.create(model=MODEL, temperature=0, max_tokens=800,
        response_format={"type": "json_object"}, messages=[{"role": "system", "content": prompt}, {"role": "user", "content": content}])
    return json.loads(response.choices[0].message.content)


def run_pipeline(bug_report_text):
    report = ask_json(NORMALIZE_PROMPT, bug_report_text)
    expected = {"title", "steps_to_reproduce", "expected_behavior", "actual_behavior", "severity", "environment"}
    if set(report) != expected:
        raise ValueError("Normalized report did not match the required structure.")
    gaps = ask_json(GAPS_PROMPT, json.dumps(report, indent=2))
    if set(gaps) != {"gaps"} or not isinstance(gaps["gaps"], list):
        raise ValueError("Gap-check response must contain only a gaps list.")
    response = client.chat.completions.create(model=MODEL, temperature=0.1, max_tokens=600,
        messages=[{"role": "system", "content": PLAN_PROMPT}, {"role": "user", "content": json.dumps({"report": report, "gap_check": gaps}, indent=2)}])
    return report, gaps["gaps"], response.choices[0].message.content.strip()


if __name__ == "__main__":
    bug_report = input("Bug report: ").strip()
    if not bug_report:
        raise ValueError("Bug report text is required.")
    report, gaps, plan = run_pipeline(bug_report)
    print("\nStructured report:\n" + json.dumps(report, indent=2))
    print("\nFlagged gaps:\n" + json.dumps(gaps, indent=2))
    print("\nPrioritized fix plan:\n" + plan)
