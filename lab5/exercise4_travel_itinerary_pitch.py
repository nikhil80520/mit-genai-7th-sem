"""Exercise 4: Travel preferences to a structured trip profile and pitch."""
import os

from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY is missing from .env")
client = Groq(api_key=api_key)
MODEL = "openai/gpt-oss-20b"


def call_model(prompt_value):
    messages = [{"role": message.type if message.type in {"system", "user", "assistant"} else "user", "content": message.content} for message in prompt_value.to_messages()]
    response = client.chat.completions.create(model=MODEL, temperature=0.1, max_tokens=900, messages=messages)
    return response.choices[0].message.content.strip()




class TripProfile(BaseModel):
    destination_type: str = Field(description="Type of destination, or 'Not stated'")
    budget_level: str = Field(description="Budget level, or 'Not stated'")
    trip_duration: str = Field(description="Duration, or 'Not stated'")
    interests: list[str] = Field(description="Interests explicitly stated")


parser = PydanticOutputParser(pydantic_object=TripProfile)
profile_prompt = PromptTemplate.from_template("Extract a trip profile from the travel preference. Do not infer unmentioned details.\n{format_instructions}\nPreference:\n{travel_preference_text}")
pitch_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an enthusiastic travel agent. Write a short persuasive itinerary pitch based only on the supplied trip profile. Do not invent destinations, prices, or activities."),
    ("user", "Trip profile:\n{profile}"),
])
pitch_parser = StrOutputParser()


def run_pipeline(travel_preference_text):
    profile_message = profile_prompt.invoke({"travel_preference_text": travel_preference_text, "format_instructions": parser.get_format_instructions()})
    profile = parser.parse(call_model(profile_message))
    pitch_message = pitch_prompt.invoke({"profile": profile.model_dump_json(indent=2)})
    return profile, pitch_parser.parse(call_model(pitch_message))


if __name__ == "__main__":
    preference = input("Travel preference: ").strip()
    if not preference:
        raise ValueError("Travel preference is required.")
    profile, pitch = run_pipeline(preference)
    print("\nStructured trip profile:\n" + profile.model_dump_json(indent=2))
    print("\nItinerary pitch:\n" + pitch)
