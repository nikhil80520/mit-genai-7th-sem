"""Exercise 6: Structured expense splitter, manual and model calls."""
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

load_dotenv(); model = ChatGroq(model="openai/gpt-oss-20b", api_key=os.getenv("GROQ_API_KEY"), temperature=0)

class SplitInput(BaseModel):
    total_amount: float = Field(gt=0)
    num_people: int = Field(gt=0)

def split_expense(total_amount, num_people):
    """Split a bill equally among people."""
    return f"Each person owes ₹{total_amount / num_people:,.2f}"

split_tool = StructuredTool.from_function(split_expense, args_schema=SplitInput, name="split_expense", description="Split a total bill equally.")

def run(user_query, total_amount, num_people):
    manual = split_tool.invoke({"total_amount": total_amount, "num_people": num_people})
    bound = model.bind_tools([split_tool]); first = bound.invoke(user_query)
    results = [ToolMessage(content=str(split_tool.invoke(c["args"])), tool_call_id=c["id"]) for c in first.tool_calls]
    final = bound.invoke([HumanMessage(content=user_query), first, *results])
    return manual, first.tool_calls, [x.content for x in results], final.content

if __name__ == "__main__":
    total = float(input("Total amount: ")); people = int(input("Number of people: ")); query = input("Question: ").strip()
    manual, calls, result, answer = run(query, total, people)
    print("Manual result:", manual); print("Tool calls:", calls); print("Bound result:", result); print("Final answer:", answer)
