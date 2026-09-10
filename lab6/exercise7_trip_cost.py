"""Exercise 7: Three independent tools for a trip cost estimate."""
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool

load_dotenv(); model = ChatGroq(model="openai/gpt-oss-20b", api_key=os.getenv("GROQ_API_KEY"), temperature=0)

@tool
def get_flight_cost(origin: str, destination: str) -> str:
    """Get a rough round-trip flight cost in INR."""
    return f"Estimated return flight {origin} to {destination}: ₹8,000"
@tool
def get_hotel_cost(city: str, nights: int) -> str:
    """Get a rough hotel cost in INR."""
    return f"Hotel in {city} for {nights} nights: ₹{3500 * nights:,}"
@tool
def get_food_budget(city: str, days: int) -> str:
    """Get a rough food budget in INR."""
    return f"Food in {city} for {days} days: ₹{1200 * days:,}"

def run(user_query):
    tools = [get_flight_cost, get_hotel_cost, get_food_budget]; lookup = {x.name: x for x in tools}; bound = model.bind_tools(tools); first = bound.invoke(user_query)
    results = [ToolMessage(content=str(lookup[c["name"]].invoke(c["args"])), tool_call_id=c["id"]) for c in first.tool_calls]
    final = bound.invoke([HumanMessage(content=user_query), first, *results]); return first.tool_calls, [x.content for x in results], final.content

if __name__ == "__main__":
    calls, results, answer = run(input("Trip question: ").strip())
    print("Tool calls:", calls); print("Tool results:", results); print("Final answer:", answer)
