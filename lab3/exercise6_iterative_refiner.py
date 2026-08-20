"""Exercise 6: Refine a draft for one issue over at least three rounds."""
import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY is missing from .env")
client = Groq(api_key=api_key)


SYSTEM_PROMPT = """You are an editor. Revise a draft to fix only the specified
issue while preserving its meaning and useful details. Return only the revised
draft, without commentary, headings, or quotation marks.
Output format: return only the revised draft, without commentary, headings,
or quotation marks."""


def refine(draft_text, issue_to_fix, rounds=3):
    if rounds < 3:
        raise ValueError("The exercise requires at least 3 rounds.")
    current = draft_text
    for round_number in range(1, rounds + 1):
        prompt = (
            f"Issue to fix: {issue_to_fix}\n"
            f"Round: {round_number} of {rounds}\n"
            f"Draft:\n{current}"
        )
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            temperature=0.2,
            max_tokens=600,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        )
        current = response.choices[0].message.content.strip()
    return current


if __name__ == "__main__":
    draft = input("Draft text: ").strip()
    issue = input("One issue to fix: ").strip()
    print(refine(draft, issue))