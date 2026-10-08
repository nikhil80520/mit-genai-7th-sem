"""Recommend exactly one college club from free-text student interests."""
import json, os
from dotenv import load_dotenv
from groq import Groq

CLUBS = {
    "Coding and AI Club": "programming, apps, robotics, AI, hackathons",
    "Cultural Club": "dance, music, theatre, art, events",
    "Photography and Media Club": "photography, film, editing, design",
    "Sports Club": "fitness, cricket, football, badminton",
    "Literary and Debate Club": "writing, reading, speaking, quizzes",
    "Social Service Club": "volunteering, teaching, environment, community work",
}

def recommend(client, interests):
    prompt = f'''Student interests: {interests!r}
Choose the ONE best club from this exact list: {json.dumps(CLUBS)}.
Return JSON only: {{"club":"exact list name","reason":"one friendly sentence of at most 22 words"}}.'''
    reply = client.chat.completions.create(
        model="llama-3.3-70b-versatile", temperature=0.2, max_tokens=100,
        response_format={"type": "json_object"},
        messages=[{"role": "system", "content": "You are a helpful college student mentor."}, {"role": "user", "content": prompt}],
    )
    result = json.loads(reply.choices[0].message.content)
    if result.get("club") not in CLUBS or not result.get("reason"):
        raise ValueError("Invalid response received; please try again.")
    return result

load_dotenv()
key = os.getenv("GROQ_API_KEY")
if not key: raise RuntimeError("GROQ_API_KEY is missing from .env")
client = Groq(api_key=key)
print("=== College Club Finder ===\nDescribe your interests. Type 'exit' to quit.")
while True:
    interests = input("\nYour interests: ").strip()
    if interests.lower() in {"exit", "quit"}: break
    if len(interests) < 8:
        print("Please add detail, e.g. 'I like programming and making websites'.")
        continue
    try:
        item = recommend(client, interests)
        print(f"\nRecommended club: {item['club']}\nWhy: {item['reason']}")
    except (ValueError, json.JSONDecodeError) as error: print(f"Could not recommend a club: {error}")
