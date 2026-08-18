"""Generate and validate exactly three Instagram captions."""
import json, os, re
from dotenv import load_dotenv
from groq import Groq

def is_valid(text):
    return len(text.split()) < 30 and bool(re.search(r"#[A-Za-z][A-Za-z0-9_]*", text))

load_dotenv()
key = os.getenv("GROQ_API_KEY")
if not key: raise RuntimeError("GROQ_API_KEY is missing from .env")
fest = input("Fest name: ").strip()
theme = input("Fest theme: ").strip()
if not fest or not theme: raise ValueError("Both fest name and theme are required.")
prompt = f'''Create Instagram captions for the college fest {fest!r}, themed {theme!r}.
Return JSON only: {{"captions":["...","...","..."]}}.
Rules: exactly three distinct captions, each under 30 words, each with a relevant hashtag. No text outside JSON.'''
reply = Groq(api_key=key).chat.completions.create(
    model="llama-3.3-70b-versatile", messages=[{"role":"user","content":prompt}],
    response_format={"type":"json_object"}, temperature=0.8, max_tokens=220)
captions = json.loads(reply.choices[0].message.content).get("captions", [])
if len(captions) != 3 or not all(isinstance(c, str) and is_valid(c) for c in captions):
    raise ValueError("Generated output did not meet the caption requirements. Run it again.")
print("\n=== Caption Options ===")
for index, caption in enumerate(captions, 1): print(f"{index}. {caption} ({len(caption.split())} words)")
