"""Exercise 5: Translate a sentence at a requested formality level."""
import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY is missing from .env")
client = Groq(api_key=api_key)


SYSTEM_PROMPT = """You are a precise translator. Translate the user's sentence
into the requested target language. Match the requested formality exactly:
formal, neutral, or informal. Preserve meaning, names, numbers, and punctuation
where natural.
Output format: return only the translated sentence, with no explanation,
labels, quotation marks, or additional text."""


def translate(sentence, target_language, formality):
    allowed = {"formal", "neutral", "informal"}
    if formality.lower() not in allowed:
        raise ValueError("formality must be formal, neutral, or informal.")
    prompt = f"""Target language: {target_language}
Formality: {formality.lower()}
Sentence: {sentence}"""
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        temperature=0.1,
        max_tokens=300,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    sentence = input("Sentence: ").strip()
    language = input("Target language: ").strip()
    formality = input("Formality (formal/neutral/informal): ").strip()
    print(translate(sentence, language, formality))