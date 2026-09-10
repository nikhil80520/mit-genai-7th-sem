"""Exercise 2: Validated EMI calculator StructuredTool."""
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

load_dotenv()
model = ChatGroq(model="openai/gpt-oss-20b", api_key=os.getenv("GROQ_API_KEY"), temperature=0)

class EMIInput(BaseModel):
    principal: float = Field(gt=0)
    annual_rate: float = Field(ge=0, le=30)
    tenure_months: int = Field(gt=0)

def calculate_emi(principal, annual_rate, tenure_months):
    """Calculate monthly loan EMI."""
    monthly_rate = annual_rate / 1200
    emi = principal / tenure_months if monthly_rate == 0 else principal * monthly_rate * (1 + monthly_rate) ** tenure_months / ((1 + monthly_rate) ** tenure_months - 1)
    return f"Monthly EMI: ₹{emi:,.2f}"

emi_tool = StructuredTool.from_function(calculate_emi, args_schema=EMIInput, name="calculate_emi", description="Calculate loan EMI.")

def run(user_query):
    bound = model.bind_tools([emi_tool]); first = bound.invoke(user_query)
    results = [ToolMessage(content=str(emi_tool.invoke(call["args"])), tool_call_id=call["id"]) for call in first.tool_calls]
    final = bound.invoke([HumanMessage(content=user_query), first, *results])
    return first.tool_calls, [x.content for x in results], final.content

if __name__ == "__main__":
    calls, result, answer = run(input("Question: ").strip())
    print("Tool calls:", calls); print("Tool result:", result); print("Final answer:", answer)
