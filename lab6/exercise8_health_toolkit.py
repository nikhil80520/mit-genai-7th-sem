"""Exercise 8: BMI and calorie StructuredTools grouped in a toolkit."""
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

load_dotenv(); model = ChatGroq(model="openai/gpt-oss-20b", api_key=os.getenv("GROQ_API_KEY"), temperature=0)

class BMIInput(BaseModel): weight_kg: float = Field(gt=0); height_cm: float = Field(gt=0)
class CalorieInput(BaseModel):
    weight_kg: float = Field(gt=0); height_cm: float = Field(gt=0); age: int = Field(gt=0); activity_level: str
def calculate_bmi(weight_kg, height_cm): return f"BMI: {weight_kg / (height_cm / 100) ** 2:.1f}"
def calculate_daily_calories(weight_kg, height_cm, age, activity_level):
    factors = {"low": 1.2, "light": 1.375, "moderate": 1.55, "active": 1.725}
    return f"Estimated daily calories: {int((10 * weight_kg + 6.25 * height_cm - 5 * age + 5) * factors.get(activity_level.lower(), 1.2))} kcal"

class HealthToolkit:
    def get_tools(self):
        return [StructuredTool.from_function(calculate_bmi, args_schema=BMIInput), StructuredTool.from_function(calculate_daily_calories, args_schema=CalorieInput)]

def run(user_query):
    tools = HealthToolkit().get_tools(); lookup = {x.name: x for x in tools}; bound = model.bind_tools(tools); first = bound.invoke(user_query)
    results = [ToolMessage(content=str(lookup[c["name"]].invoke(c["args"])), tool_call_id=c["id"]) for c in first.tool_calls]
    final = bound.invoke([HumanMessage(content=user_query), first, *results]); return [x.name for x in tools], first.tool_calls, [x.content for x in results], final.content

if __name__ == "__main__":
    names, calls, results, answer = run(input("Health question: ").strip())
    print("Toolkit:", names); print("Tool calls:", calls); print("Tool results:", results); print("Final answer:", answer)
