"""Exercise 2: Extract article claims, then create a fact card from them."""
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

CLAIMS_PROMPT = """Extract the article's core factual claims. Return valid JSON only
in the form {"claims": ["claim", ...]}. Preserve uncertainty and attribution.
Do not add facts, interpretations, or claims not supported by the article."""
CARD_PROMPT = """Create a short fact card using only the supplied claims. Return exactly:
Headline: <neutral headline>
- <fact>
- <fact>
- <fact>
Source confidence: <brief note based only on the claims' attribution and certainty>
Do not introduce facts not in the claims."""


def extract_claims(article_text):
    response = client.chat.completions.create(model=MODEL, temperature=0, max_tokens=600,
        response_format={"type": "json_object"}, messages=[{"role": "system", "content": CLAIMS_PROMPT}, {"role": "user", "content": article_text}])
    result = json.loads(response.choices[0].message.content)
    if set(result) != {"claims"} or not isinstance(result["claims"], list):
        raise ValueError("Claims response must contain only a claims list.")
    return result["claims"]


def create_fact_card(claims):
    response = client.chat.completions.create(model=MODEL, temperature=0.1, max_tokens=400,
        messages=[{"role": "system", "content": CARD_PROMPT}, {"role": "user", "content": json.dumps({"claims": claims}, indent=2)}])
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    article = input("News article: ").strip()
    if not article:
        raise ValueError("Article text is required.")
    claims = extract_claims(article)
    print("\nExtracted claims:\n" + json.dumps(claims, indent=2))
    print("\nFact card:\n" + create_fact_card(claims))
