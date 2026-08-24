"""Exercise 1: Turn a job posting into candidate outreach in two LLM stages."""
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

REQUIREMENTS_PROMPT = """Extract job requirements from the supplied posting.
Return valid JSON only with exactly these keys: title, required_skills,
preferred_skills, experience, location, and responsibilities. Values unavailable
in the posting must be null; lists must contain only stated items. Do not infer."""
OUTREACH_PROMPT = """Write a concise, warm, professional recruiting outreach message.
Use the supplied structured job requirements and candidate profile only. Mention
only genuine overlaps; do not invent candidate facts or job details. Return only
the message, without a subject line or commentary."""


def extract_requirements(job_posting_text):
    response = client.chat.completions.create(
        model=MODEL, temperature=0, max_tokens=600,
        response_format={"type": "json_object"},
        messages=[{"role": "system", "content": REQUIREMENTS_PROMPT},
                  {"role": "user", "content": job_posting_text}],
    )
    result = json.loads(response.choices[0].message.content)
    expected = {"title", "required_skills", "preferred_skills", "experience", "location", "responsibilities"}
    if set(result) != expected:
        raise ValueError("Requirements response did not match the required structure.")
    return result


def generate_outreach(structured_requirements, candidate_profile):
    prompt = f"""Structured job requirements:\n{json.dumps(structured_requirements, indent=2)}

Candidate profile:\n{candidate_profile}"""
    response = client.chat.completions.create(
        model=MODEL, temperature=0.3, max_tokens=400,
        messages=[{"role": "system", "content": OUTREACH_PROMPT}, {"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()


def run_pipeline(job_posting_text, candidate_profile):
    requirements = extract_requirements(job_posting_text)
    return requirements, generate_outreach(requirements, candidate_profile)


if __name__ == "__main__":
    posting = input("Job posting: ").strip()
    profile = input("Candidate profile: ").strip()
    if not posting or not profile:
        raise ValueError("Job posting and candidate profile are required.")
    requirements, outreach = run_pipeline(posting, profile)
    print("\nStructured requirements:\n" + json.dumps(requirements, indent=2))
    print("\nPersonalized outreach:\n" + outreach)
