"""Debug Python code using the code and its actual error message."""
import json, os
from dotenv import load_dotenv
from groq import Groq

def multiline():
    print("Paste broken Python code; enter END on a line by itself when finished.")
    lines = []
    while True:
        line = input()
        if line == "END": return "\n".join(lines)
        lines.append(line)

load_dotenv()
key = os.getenv("GROQ_API_KEY")
if not key: raise RuntimeError("GROQ_API_KEY is missing from .env")
code = multiline()
error = input("Error message: ").strip()
if not code or not error: raise ValueError("Broken code and error message are both required.")
prompt = f'''Act as a precise Python debugger. Make the smallest correction that fixes the supplied error; preserve program intent.
BROKEN CODE:\n{code}\n\nERROR MESSAGE:\n{error}
Return JSON only: {{"corrected_code":"complete code","explanation":"one sentence, maximum 25 words"}}.'''
reply = Groq(api_key=key).chat.completions.create(
    model="llama-3.3-70b-versatile", messages=[{"role":"user","content":prompt}],
    response_format={"type":"json_object"}, temperature=0, max_tokens=700)
result = json.loads(reply.choices[0].message.content)
if not result.get("corrected_code") or not result.get("explanation"): raise ValueError("Incomplete debugging response.")
print("\n=== CORRECTED CODE ===\n" + result["corrected_code"])
print("\n=== EXPLANATION ===\n" + result["explanation"])
