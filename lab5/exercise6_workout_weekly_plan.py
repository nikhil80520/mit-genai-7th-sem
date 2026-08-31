"""Exercise 6: Fitness goal to parsed details and a weekly workout plan."""
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY is missing from .env")
MODEL = "openai/gpt-oss-20b"
model = ChatGroq(model=MODEL, api_key=api_key, temperature=0.1, max_tokens=900)




class FitnessGoal(BaseModel):
    goal_type: str = Field(description="Primary goal, or 'Not stated'")
    fitness_level: str = Field(description="Current fitness level, or 'Not stated'")
    days_available: int | None = Field(description="Days available per week, if stated")
    equipment_access: str = Field(description="Equipment access, or 'Not stated'")


class WorkoutDay(BaseModel):
    day: str
    workout: str
    duration_minutes: int | None


class WeeklyWorkoutPlan(BaseModel):
    weekly_plan: list[WorkoutDay]


goal_parser = PydanticOutputParser(pydantic_object=FitnessGoal)
plan_parser = PydanticOutputParser(pydantic_object=WeeklyWorkoutPlan)
goal_prompt = PromptTemplate.from_template("Extract fitness goal details from this free-form description. Do not infer details.\n{format_instructions}\nDescription:\n{fitness_goal_text}")
plan_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a certified personal trainer. Create a safe, balanced weekly plan using only the supplied goal details and requested availability. Include exactly one entry per available training day; do not provide medical advice."),
    ("user", "Goal details:\n{goal}\nRequested days per week: {days_per_week}\n{format_instructions}"),
])


def run_pipeline(fitness_goal_text, days_per_week):
    if days_per_week < 1 or days_per_week > 7:
        raise ValueError("days_per_week must be between 1 and 7.")
    goal_message = goal_prompt.invoke({"fitness_goal_text": fitness_goal_text, "format_instructions": goal_parser.get_format_instructions()})
    result = model.invoke(goal_message)
    goal = goal_parser.invoke(result)
    plan_message = plan_prompt.invoke({"goal": goal.model_dump_json(indent=2), "days_per_week": days_per_week, "format_instructions": plan_parser.get_format_instructions()})
    result = model.invoke(plan_message)
    plan = plan_parser.invoke(result)
    return goal, plan


if __name__ == "__main__":
    goal_text = input("Fitness goal description: ").strip()
    days = int(input("Days available per week: ").strip())
    if not goal_text:
        raise ValueError("Fitness goal description is required.")
    goal, plan = run_pipeline(goal_text, days)
    print("\nExtracted goal details:\n" + goal.model_dump_json(indent=2))
    print("\nWeekly workout plan:\n" + plan.model_dump_json(indent=2))
