"""Create exactly two and five line research-abstract summaries in one run."""
import json, os
from dotenv import load_dotenv
from groq import Groq

def read_abstract():
    print("Paste the abstract; enter END on a line by itself when finished.")
    lines=[]
    while True:
        line=input()
        if line == "END": return "\n".join(lines).strip()
        lines.append(line)

load_dotenv()
key=os.getenv("GROQ_API_KEY")
if not key: raise RuntimeError("GROQ_API_KEY is missing from .env")
abstract=read_abstract()
if len(abstract.split()) < 20: raise ValueError("Please provide an abstract of at least 20 words.")
prompt=f'''Summarize this research abstract without inventing facts. Retain objective, method, main result, and conclusion where available.\n\n{abstract}\n\nReturn JSON only: {{"two_line_summary":["line 1","line 2"],"five_line_summary":["line 1","line 2","line 3","line 4","line 5"]}}. Each item must be a concise complete line.'''
reply=Groq(api_key=key).chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":prompt}], response_format={"type":"json_object"}, temperature=0.15, max_tokens=450)
result=json.loads(reply.choices[0].message.content)
two, five=result.get("two_line_summary"), result.get("five_line_summary")
if not (isinstance(two,list) and len(two)==2 and isinstance(five,list) and len(five)==5): raise ValueError("Required summary line counts were not returned.")
print("\n=== 2-LINE SUMMARY ===\n" + "\n".join(two))
print("\n=== 5-LINE SUMMARY ===\n" + "\n".join(five))
