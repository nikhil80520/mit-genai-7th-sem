"""Exercise 3: Two conversion tools; model selects the relevant one."""
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool

load_dotenv(); model = ChatGroq(model="openai/gpt-oss-20b", api_key=os.getenv("GROQ_API_KEY"), temperature=0)

@tool
def convert_temperature(value: float, from_unit: str, to_unit: str) -> str:
    """Convert Celsius and Fahrenheit temperatures."""
    value = value * 9 / 5 + 32 if from_unit.lower().startswith("c") else (value - 32) * 5 / 9
    return f"{value:.2f}° {to_unit}"

@tool
def convert_distance(value: float, from_unit: str, to_unit: str) -> str:
    """Convert kilometres and miles."""
    value = value * 0.621371 if from_unit.lower() in {"km", "kilometres", "kilometers"} else value / 0.621371
    return f"{value:.2f} {to_unit}"

def run(user_query):
    tools = [convert_temperature, convert_distance]; lookup = {tool.name: tool for tool in tools}; bound = model.bind_tools(tools); first = bound.invoke(user_query)
    results = [ToolMessage(content=str(lookup[c["name"]].invoke(c["args"])), tool_call_id=c["id"]) for c in first.tool_calls]
    final = bound.invoke([HumanMessage(content=user_query), first, *results]); return first.tool_calls, [x.content for x in results], final.content

if __name__ == "__main__":
    calls, result, answer = run(input("Question: ").strip())
    print("Tool calls:", calls); print("Tool result:", result); print("Final answer:", answer)
