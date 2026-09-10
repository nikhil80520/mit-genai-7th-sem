"""Exercise 10: Restaurant recommendation with four bound tools."""
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool

load_dotenv(); model = ChatGroq(model="openai/gpt-oss-20b", api_key=os.getenv("GROQ_API_KEY"), temperature=0)

@tool
def find_restaurants(cuisine: str, city: str) -> str:
    """Find restaurants for a cuisine and city."""; return "La Pino's, Little Italy" if cuisine.lower() == "italian" else "Cafe Central, Food Street"
@tool
def get_restaurant_rating(restaurant_name: str) -> str:
    """Get a restaurant rating out of 5."""; return f"{restaurant_name}: 4.4/5"
@tool
def check_restaurant_open(restaurant_name: str, day: str) -> str:
    """Check whether a restaurant is open on a day."""; return f"{restaurant_name} is open on {day}."
@tool
def estimate_cost_for_two(restaurant_name: str) -> str:
    """Estimate cost for two in INR."""; return f"{restaurant_name}: about ₹1,800 for two"

def run(user_query):
    tools = [find_restaurants, get_restaurant_rating, check_restaurant_open, estimate_cost_for_two]; lookup = {x.name: x for x in tools}; bound = model.bind_tools(tools); first = bound.invoke(user_query)
    results = [ToolMessage(content=str(lookup[c["name"]].invoke(c["args"])), tool_call_id=c["id"]) for c in first.tool_calls]
    final = bound.invoke([HumanMessage(content=user_query), first, *results]); return first.tool_calls, [x.content for x in results], final.content

if __name__ == "__main__":
    calls, results, answer = run(input("Restaurant question: ").strip())
    print("Tool calls:", calls); print("Tool results:", results); print("Final answer:", answer)
