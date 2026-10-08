"""Adaptive first-year tutor with explicit re-explanation tracking."""
import os, re
from dotenv import load_dotenv
from groq import Groq

CONFUSION=re.compile(r"\b(don't get it|do not get it|confused|not clear|explain again|re-?explain)\b", re.I)

def reply(client, history):
    response=client.chat.completions.create(model="llama-3.3-70b-versatile", messages=history, temperature=0.45, max_tokens=300)
    text=response.choices[0].message.content.strip()
    history.append({"role":"assistant","content":text})
    print("\nTutor: " + text + "\n")

load_dotenv()
key=os.getenv("GROQ_API_KEY")
if not key: raise RuntimeError("GROQ_API_KEY is missing from .env")
topic=input("First-year topic to learn: ").strip()
if not topic: raise ValueError("A topic is required.")
history=[
    {"role":"system","content":"You are an encouraging first-year college tutor. Give clear short explanations, simple examples, and never assume prior knowledge. On a re-explanation, use a genuinely different analogy or approach, then ask one quick check-for-understanding question."},
    {"role":"user","content":f"Give me an initial beginner-friendly explanation of {topic}."}]
client=Groq(api_key=key); count=0
reply(client, history)
print("Type a question, 'I don't get it', 'I understand', or 'exit'.")
while True:
    message=input("You: ").strip()
    low=message.lower()
    if low in {"exit","quit"}:
        print(f"Session ended. Re-explanations for {topic}: {count}"); break
    if re.search(r"\b(i understand|got it|i got it)\b", low):
        print(f"Excellent. Re-explanations for {topic}: {count}"); break
    if CONFUSION.search(message):
        count+=1
        print(f"(Re-explanation count: {count})")
        message=f"The student is confused about {topic}. Re-explain it using a new analogy or approach. This is re-explanation #{count}."
    history.append({"role":"user","content":message})
    reply(client, history)
