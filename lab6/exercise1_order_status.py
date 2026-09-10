"""Exercise 1: Order status lookup with one tool."""
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool

load_dotenv()
model = ChatGroq(model="openai/gpt-oss-20b", api_key=os.getenv("GROQ_API_KEY"), temperature=0)

@tool
def lookup_order_status(order_id: str) -> str:
    """Look up shipping status for an order ID."""
    orders = {"ORD-4521": "Shipped; expected delivery Friday", "ORD-7788": "Processing in warehouse"}
    return orders.get(order_id.upper(), "Order not found")

def run(user_query):
    bound = model.bind_tools([lookup_order_status])
    first = bound.invoke(user_query)
    results = [ToolMessage(content=str(lookup_order_status.invoke(call["args"])), tool_call_id=call["id"]) for call in first.tool_calls]
    final = bound.invoke([HumanMessage(content=user_query), first, *results])
    return first.tool_calls, [item.content for item in results], final.content

if __name__ == "__main__":
    query = input("Question: ").strip()
    calls, results, answer = run(query)
    print("Tool calls:", calls); print("Tool result:", results); print("Final answer:", answer)
