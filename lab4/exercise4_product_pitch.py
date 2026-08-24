"""Exercise 4: Expand a product idea, then pitch the structured concept."""
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

STRUCTURE_PROMPT = """Expand the product idea into a grounded structured pitch. Return
valid JSON only with exactly: problem, solution, target_user. State reasonable
assumptions as part of the wording; do not claim unsupported validation."""
INVESTOR_PROMPT = """Write one concise investor-style pitch paragraph using only the
structured pitch below. Explain the problem, solution, and target user without
inventing metrics, traction, pricing, competitors, or facts. Return only the paragraph."""


def structure_idea(product_idea):
    response = client.chat.completions.create(model=MODEL, temperature=0.3, max_tokens=500,
        response_format={"type": "json_object"}, messages=[{"role": "system", "content": STRUCTURE_PROMPT}, {"role": "user", "content": product_idea}])
    pitch = json.loads(response.choices[0].message.content)
    if set(pitch) != {"problem", "solution", "target_user"}:
        raise ValueError("Structured pitch did not contain the required fields.")
    return pitch


def write_investor_pitch(structured_pitch):
    response = client.chat.completions.create(model=MODEL, temperature=0.4, max_tokens=300,
        messages=[{"role": "system", "content": INVESTOR_PROMPT}, {"role": "user", "content": json.dumps(structured_pitch, indent=2)}])
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    idea = input("One-line product idea: ").strip()
    if not idea:
        raise ValueError("Product idea is required.")
    structured = structure_idea(idea)
    print("\nStructured pitch:\n" + json.dumps(structured, indent=2))
    print("\nInvestor pitch:\n" + write_investor_pitch(structured))
