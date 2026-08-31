"""Exercise 1: Customer review to structured complaint and support ticket."""
import os

from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY is missing from .env")
client = Groq(api_key=api_key)
MODEL = "openai/gpt-oss-20b"


def call_model(prompt_value):
    messages = [{"role": message.type if message.type in {"system", "user", "assistant"} else "user", "content": message.content} for message in prompt_value.to_messages()]
    response = client.chat.completions.create(model=MODEL, temperature=0.1, max_tokens=900, messages=messages)
    return response.choices[0].message.content.strip()




class ComplaintData(BaseModel):
    complaint: str = Field(description="Customer's core complaint, or 'Not stated'")
    product_or_feature: str = Field(description="Mentioned product or feature, or 'Not stated'")
    sentiment: str = Field(description="Positive, negative, mixed, or neutral")


complaint_parser = PydanticOutputParser(pydantic_object=ComplaintData)
extract_prompt = PromptTemplate.from_template(
    "Extract only facts from this raw customer review.\n{format_instructions}\nReview:\n{review_text}"
)
ticket_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a support ticket writer. Create a concise internal ticket using only supplied structured data. Do not invent facts."),
    ("user", "Structured complaint data:\n{complaint_data}"),
])
ticket_parser = StrOutputParser()


def run_pipeline(review_text):
    extraction = extract_prompt.invoke({"review_text": review_text, "format_instructions": complaint_parser.get_format_instructions()})
    complaint = complaint_parser.parse(call_model(extraction))
    ticket_message = ticket_prompt.invoke({"complaint_data": complaint.model_dump_json(indent=2)})
    ticket = ticket_parser.parse(call_model(ticket_message))
    return complaint, ticket


if __name__ == "__main__":
    review = input("Customer review: ").strip()
    if not review:
        raise ValueError("Review text is required.")
    complaint, ticket = run_pipeline(review)
    print("\nStructured complaint data:\n" + complaint.model_dump_json(indent=2))
    print("\nSupport ticket summary:\n" + ticket)
