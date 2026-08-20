"""Exercise 3: Extract only requested resume fields as strict JSON."""
import json
import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY is missing from .env")
client = Groq(api_key=api_key)


SYSTEM_PROMPT = """You extract fields from resume text.
Return one valid JSON object and nothing else. Use exactly the requested field
names and no additional keys. If a requested value is absent, use null.
Do not guess or infer information.
Output format: strict JSON object only, with exactly the requested keys and no
markdown, explanation, or additional text.
Example format when the requested fields are name and email:
{"name": "Jordan Lee", "email": null}"""


def extract_fields(resume_text, fields_to_extract):
    requested = [field.strip() for field in fields_to_extract if field.strip()]
    if not requested:
        raise ValueError("At least one field is required.")
    output_shape = {field: "value or null" for field in requested}
    prompt = f"""Requested fields: {json.dumps(requested)}
Expected JSON shape:
{json.dumps(output_shape, indent=2)}
Resume text:
{resume_text}"""
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        temperature=0,
        max_tokens=500,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    result = json.loads(response.choices[0].message.content)
    if set(result) != set(requested):
        raise ValueError("The response did not contain exactly the requested fields.")
    return result


if __name__ == "__main__":
    resume = input("Resume text: ").strip()
    fields = input("Fields to extract, comma separated: ").split(",")
    if not resume:
        raise ValueError("Resume text is required.")
    print(json.dumps(extract_fields(resume, fields), indent=2))