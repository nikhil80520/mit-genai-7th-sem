"""Exercise 2: Classify a customer review with one category label."""
import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY is missing from .env")
client = Groq(api_key=api_key)


SYSTEM_PROMPT = """You classify customer reviews. Choose exactly one label:
POSITIVE, NEGATIVE, MIXED, or NEUTRAL.
POSITIVE means mainly praise, NEGATIVE means mainly complaint, MIXED contains
important praise and criticism, and NEUTRAL is factual without clear sentiment.
Output format: return only the uppercase label, with no punctuation or explanation."""


def classify(review_text):
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        temperature=0.2,
        max_tokens=100,
        reasoning_effort="low",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": review_text},
        ],
    )
    label = response.choices[0].message.content.strip()
    allowed = {"POSITIVE", "NEGATIVE", "MIXED", "NEUTRAL"}
    if label not in allowed:
        raise ValueError(f"Unexpected category returned: {label!r}")
    return label


if __name__ == "__main__":
    review = input("Customer review: ").strip()
    if not review:
        raise ValueError("A customer review is required.")
    print(classify(review))