"""Exercise 1: Generate a consistent doctor's summary from consultation notes."""
import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY is missing from .env")
client = Groq(api_key=api_key)


SYSTEM_PROMPT = """You convert raw consultation notes into a concise clinical summary.
Use only information present in the notes. Do not invent symptoms, diagnoses, tests,
medicines, or advice. Keep the wording professional and easy to scan.

Always return exactly this format and nothing else:
Symptoms: <observed symptoms or 'Not documented'>
Diagnosis: <diagnosis or 'Not documented'>
Recommendation: <recommendation or 'Not documented'>"""


def build_prompt(patient_name, patient_notes):
    prompt_template = """Patient name: {patient_name}
Raw consultation notes:
{patient_notes}"""
    return prompt_template.format(
        patient_name=patient_name,
        patient_notes=patient_notes,
    )


if __name__ == "__main__":
    name = input("Patient name: ").strip()
    notes = input("Consultation notes: ").strip()
    if not name or not notes:
        raise ValueError("Patient name and consultation notes are required.")
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        temperature=0.2,
        max_tokens=500,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_prompt(name, notes)},
        ],
    )
    print(response.choices[0].message.content.strip())