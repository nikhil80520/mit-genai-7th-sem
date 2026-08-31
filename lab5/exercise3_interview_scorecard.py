"""Exercise 3: Interview transcript to evidence-based hiring scorecard."""
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




class AnswerPair(BaseModel):
    question: str
    answer: str


class ExtractedAnswers(BaseModel):
    answers: list[AnswerPair]


class SkillEvaluation(BaseModel):
    skill: str
    demonstrated: bool
    evidence_or_gap: str


class EvaluationResult(BaseModel):
    evaluations: list[SkillEvaluation]


class ScorecardRow(BaseModel):
    skill: str
    rating: str
    evidence_or_gap: str


class HiringScorecard(BaseModel):
    scorecard_rows: list[ScorecardRow]
    overall_recommendation: str


answers_parser = PydanticOutputParser(pydantic_object=ExtractedAnswers)
evaluation_parser = PydanticOutputParser(pydantic_object=EvaluationResult)
scorecard_parser = PydanticOutputParser(pydantic_object=HiringScorecard)
answers_prompt = PromptTemplate.from_template("Extract each interview question and the candidate's answer. Do not infer missing answers.\n{format_instructions}\nTranscript:\n{transcript_text}")
evaluation_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a technical interviewer evaluating skill evidence. Evaluate only the supplied answers, and flag skills not clearly demonstrated."),
    ("user", "Skills to assess: {skills}\nCandidate answers:\n{answers}\n{format_instructions}"),
])
scorecard_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a hiring panel coordinator. Create an evidence-based structured scorecard from the supplied evaluation only. Do not add evidence."),
    ("user", "Skill evaluation:\n{evaluations}\n{format_instructions}"),
])


def run_pipeline(transcript_text, skills_to_assess):
    answers_message = answers_prompt.invoke({"transcript_text": transcript_text, "format_instructions": answers_parser.get_format_instructions()})
    result = model.invoke(answers_message)
    answers = answers_parser.invoke(result)
    evaluation_message = evaluation_prompt.invoke({"skills": skills_to_assess, "answers": answers.model_dump_json(indent=2), "format_instructions": evaluation_parser.get_format_instructions()})
    result = model.invoke(evaluation_message)
    evaluations = evaluation_parser.invoke(result)
    scorecard_message = scorecard_prompt.invoke({"evaluations": evaluations.model_dump_json(indent=2), "format_instructions": scorecard_parser.get_format_instructions()})
    result = model.invoke(scorecard_message)
    scorecard = scorecard_parser.invoke(result)
    return answers, evaluations, scorecard


if __name__ == "__main__":
    transcript = input("Interview transcript: ").strip()
    skills = input("Skills to assess (comma separated): ").strip()
    if not transcript or not skills:
        raise ValueError("Transcript and skills are required.")
    answers, evaluations, scorecard = run_pipeline(transcript, skills)
    print("\nExtracted answers:\n" + answers.model_dump_json(indent=2))
    print("\nFlagged skill evaluation:\n" + evaluations.model_dump_json(indent=2))
    print("\nFinal scorecard:\n" + scorecard.model_dump_json(indent=2))
