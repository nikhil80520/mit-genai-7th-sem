"""Exercise 3: Convert a meeting transcript into a structured task table."""
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

DISCUSSION_PROMPT = """Summarize what was discussed in the meeting transcript.
Return valid JSON only: {"discussion": ["topic or decision", ...]}. Use only
the transcript and retain uncertainty where present."""
ACTION_PROMPT = """Identify action items from the supplied discussion only. Return valid
JSON only: {"action_items": [{"task": "...", "owner": "name or null", "deadline": "date or null", "flags": ["missing owner", "missing deadline"]}]}. Flag every missing owner or deadline. Do not invent details."""
TABLE_PROMPT = """Format the supplied action items only as a Markdown table with exactly
these columns: Task | Owner | Deadline | Flags. Show missing values as 'Missing'.
Return only the table."""


def ask_json(system_prompt, content):
    response = client.chat.completions.create(model=MODEL, temperature=0, max_tokens=800,
        response_format={"type": "json_object"}, messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": content}])
    return json.loads(response.choices[0].message.content)


def run_pipeline(transcript_text):
    discussion = ask_json(DISCUSSION_PROMPT, transcript_text)
    if set(discussion) != {"discussion"}:
        raise ValueError("Discussion response has an unexpected structure.")
    actions = ask_json(ACTION_PROMPT, json.dumps(discussion, indent=2))
    if set(actions) != {"action_items"}:
        raise ValueError("Action-item response has an unexpected structure.")
    response = client.chat.completions.create(model=MODEL, temperature=0, max_tokens=600,
        messages=[{"role": "system", "content": TABLE_PROMPT}, {"role": "user", "content": json.dumps(actions, indent=2)}])
    return discussion["discussion"], actions["action_items"], response.choices[0].message.content.strip()


if __name__ == "__main__":
    transcript = input("Meeting transcript: ").strip()
    if not transcript:
        raise ValueError("Transcript text is required.")
    discussion, actions, table = run_pipeline(transcript)
    print("\nDiscussion summary:\n" + json.dumps(discussion, indent=2))
    print("\nFlagged action items:\n" + json.dumps(actions, indent=2))
    print("\nTask table:\n" + table)
