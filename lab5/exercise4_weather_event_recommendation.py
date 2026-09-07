"""Exercise 4: Event plan to weather-adjusted recommendation."""
import json
import os

import requests
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from pydantic import BaseModel


load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY is missing from .env")
model = ChatGroq(model="openai/gpt-oss-20b", api_key=api_key, temperature=0)


class EventDetails(BaseModel):
    event_type: str
    event_date: str
    location: str
    indoor_outdoor_preference: str


class WeatherData(BaseModel):
    temperature: float
    precipitation_chance: float
    conditions: str


event_parser = PydanticOutputParser(pydantic_object=EventDetails)
weather_parser = PydanticOutputParser(pydantic_object=WeatherData)
recommendation_parser = StrOutputParser()

event_template = PromptTemplate(
    template="Extract event details. Use date format YYYY-MM-DD.\n{format_instruction}\nEvent: {event}",
    input_variables=["event"],
    partial_variables={"format_instruction": event_parser.get_format_instructions()},
)
weather_url_template = PromptTemplate.from_template(
    "https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}"
    "&daily=temperature_2m_max,precipitation_probability_max,weather_code"
    "&timezone=auto&start_date={date}&end_date={date}"
)
recommendation_template = ChatPromptTemplate.from_messages([
    ("system", "You are an event planning assistant. Recommend: proceed as planned, reschedule, or move indoors. Use only the provided details."),
    ("human", "Event details: {event_details}\nWeather data: {weather_data}"),
])


def get_weather(event):
    place = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": event.location, "count": 1}, timeout=20,
    ).json()["results"][0]
    weather_url = weather_url_template.invoke({
        "latitude": place["latitude"], "longitude": place["longitude"], "date": event.event_date,
    }).to_string()
    daily = requests.get(weather_url, timeout=20).json()["daily"]
    weather_json = json.dumps({
        "temperature": daily["temperature_2m_max"][0],
        "precipitation_chance": daily["precipitation_probability_max"][0],
        "conditions": f"Weather code {daily['weather_code'][0]}",
    })
    return weather_parser.invoke(weather_json)


def run_pipeline(event_description_text):
    prompt = event_template.invoke({"event": event_description_text})
    event = event_parser.invoke(model.invoke(prompt))
    weather = get_weather(event)
    prompt = recommendation_template.invoke({
        "event_details": event.model_dump_json(), "weather_data": weather.model_dump_json(),
    })
    recommendation = recommendation_parser.invoke(model.invoke(prompt))
    return event, weather, recommendation


if __name__ == "__main__":
    description = input("Event description: ").strip()
    event, weather, recommendation = run_pipeline(description)
    print("\nEvent details:\n", event)
    print("\nWeather data:\n", weather)
    print("\nRecommendation:\n", recommendation)
