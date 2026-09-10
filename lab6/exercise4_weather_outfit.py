"""Exercise 4: Chained weather and outfit tools."""
import json
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool

load_dotenv(); model = ChatGroq(model="openai/gpt-oss-20b", api_key=os.getenv("GROQ_API_KEY"), temperature=0)

@tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    weather = {"mumbai": {"temperature": 30, "conditions": "rainy"}, "delhi": {"temperature": 34, "conditions": "sunny"}}
    return json.dumps(weather.get(city.lower(), {"temperature": 25, "conditions": "partly cloudy"}))

@tool
def recommend_outfit(temperature: float, conditions: str) -> str:
    """Recommend an outfit using temperature and weather conditions."""
    if "rain" in conditions.lower(): return "Wear light clothes, waterproof shoes, and carry an umbrella."
    return "Wear breathable casual clothes and comfortable shoes." if temperature >= 25 else "Wear layers and a light jacket."

def run(user_query):
    weather_model = model.bind_tools([get_weather]); first = weather_model.invoke(user_query)
    weather_results = [ToolMessage(content=str(get_weather.invoke(c["args"])), tool_call_id=c["id"]) for c in first.tool_calls]
    outfit_model = model.bind_tools([recommend_outfit])
    second = outfit_model.invoke([HumanMessage(content=user_query), first, *weather_results, HumanMessage(content="Use the fetched weather to call recommend_outfit.")])
    outfit_results = [ToolMessage(content=str(recommend_outfit.invoke(c["args"])), tool_call_id=c["id"]) for c in second.tool_calls]
    final = outfit_model.invoke([HumanMessage(content=user_query), first, *weather_results, second, *outfit_results])
    return first.tool_calls, [x.content for x in weather_results], second.tool_calls, [x.content for x in outfit_results], final.content

if __name__ == "__main__":
    first, weather, second, outfit, answer = run(input("Question: ").strip())
    print("Weather tool call:", first); print("Weather:", weather); print("Outfit tool call:", second); print("Outfit:", outfit); print("Final answer:", answer)
