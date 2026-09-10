"""Exercise 9: Calendar, timezone, and booking tools with partial use."""
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool

load_dotenv(); model = ChatGroq(model="openai/gpt-oss-20b", api_key=os.getenv("GROQ_API_KEY"), temperature=0)

@tool
def check_calendar_availability(person: str, date: str) -> str:
    """Check a person's calendar availability."""; return f"{person} is available on {date}."
@tool
def get_timezone_offset(city: str) -> str:
    """Get a city's UTC offset."""; return {"mumbai": "UTC+5:30", "london": "UTC+1"}.get(city.lower(), "UTC+0")
@tool
def book_meeting(person: str, date: str, time: str) -> str:
    """Book a meeting."""; return f"Meeting booked with {person} on {date} at {time}."

def ask(query):
    tools = [check_calendar_availability, get_timezone_offset, book_meeting]; lookup = {x.name: x for x in tools}; bound = model.bind_tools(tools); first = bound.invoke(query)
    results = [ToolMessage(content=str(lookup[c["name"]].invoke(c["args"])), tool_call_id=c["id"]) for c in first.tool_calls]
    final = bound.invoke([HumanMessage(content=query), first, *results]); return first.tool_calls, [x.content for x in results], final.content

if __name__ == "__main__":
    availability_query = input("Availability-only question: ").strip(); booking_query = input("Booking question: ").strip()
    for label, query in [("Availability", availability_query), ("Booking", booking_query)]:
        calls, results, answer = ask(query); print(f"\n{label} tool calls:", calls); print("Results:", results); print("Final answer:", answer)
