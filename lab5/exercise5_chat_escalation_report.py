"""Exercise 5: Support chat log to escalation-ready report."""
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY is missing from .env")
MODEL = "openai/gpt-oss-20b"
model = ChatGroq(model=MODEL, api_key=api_key, temperature=0.1, max_tokens=900)




class ChatSummary(BaseModel):
    issue: str = Field(description="Customer issue, or 'Not stated'")
    customer_tone: str = Field(description="Customer tone, or 'Not stated'")
    resolution_attempted: str = Field(description="Attempted resolution, or 'Not stated'")


class EscalationReadiness(BaseModel):
    missing_fields: list[str]
    is_ready_to_escalate: bool


summary_parser = PydanticOutputParser(pydantic_object=ChatSummary)
readiness_parser = PydanticOutputParser(pydantic_object=EscalationReadiness)
summary_prompt = PromptTemplate.from_template("Normalize this support chat log into the requested structured summary. Do not add facts.\n{format_instructions}\nChat log:\n{chat_log_text}")
readiness_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an escalation-readiness reviewer. Identify information required to escalate that is missing from the supplied summary, including account ID or error code when relevant. Do not invent values."),
    ("user", "Structured support summary:\n{summary}\n{format_instructions}"),
])
report_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a support operations lead. Write a concise prioritized escalation report based only on the structured summary and readiness check. Clearly list gaps needing follow-up."),
    ("user", "Summary:\n{summary}\nReadiness check:\n{readiness}"),
])
report_parser = StrOutputParser()


def run_pipeline(chat_log_text):
    summary_message = summary_prompt.invoke({"chat_log_text": chat_log_text, "format_instructions": summary_parser.get_format_instructions()})
    result = model.invoke(summary_message)
    summary = summary_parser.invoke(result)
    readiness_message = readiness_prompt.invoke({"summary": summary.model_dump_json(indent=2), "format_instructions": readiness_parser.get_format_instructions()})
    result = model.invoke(readiness_message)
    readiness = readiness_parser.invoke(result)
    report_message = report_prompt.invoke({"summary": summary.model_dump_json(indent=2), "readiness": readiness.model_dump_json(indent=2)})
    result = model.invoke(report_message)
    report = report_parser.invoke(result)
    return summary, readiness, report


if __name__ == "__main__":
    chat_log = input("Support chat log: ").strip()
    if not chat_log:
        raise ValueError("Chat log text is required.")
    summary, readiness, report = run_pipeline(chat_log)
    print("\nStructured summary:\n" + summary.model_dump_json(indent=2))
    print("\nFlagged gaps:\n" + readiness.model_dump_json(indent=2))
    print("\nPrioritized escalation report:\n" + report)
