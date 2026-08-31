"""Exercise 2: Research abstract to structured extraction and lay summary."""
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




class ResearchExtraction(BaseModel):
    research_question: str = Field(description="Research question or 'Not stated'")
    method: str = Field(description="Method used or 'Not stated'")
    key_finding: str = Field(description="Key finding or 'Not stated'")


parser = PydanticOutputParser(pydantic_object=ResearchExtraction)
extract_prompt = PromptTemplate.from_template("Extract information from this abstract without adding facts.\n{format_instructions}\nAbstract:\n{abstract_text}")
summary_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a science communicator explaining to a general audience. Write a clear, short summary using only the supplied extraction."),
    ("user", "Structured research extraction:\n{extraction}"),
])
summary_parser = StrOutputParser()


def run_pipeline(abstract_text):
    extraction_message = extract_prompt.invoke({"abstract_text": abstract_text, "format_instructions": parser.get_format_instructions()})
    result = model.invoke(extraction_message)
    extraction = parser.invoke(result)
    summary_message = summary_prompt.invoke({"extraction": extraction.model_dump_json(indent=2)})
    result = model.invoke(summary_message)
    return extraction, summary_parser.invoke(result)


if __name__ == "__main__":
    abstract = input("Paper abstract: ").strip()
    if not abstract:
        raise ValueError("Abstract text is required.")
    extracted, summary = run_pipeline(abstract)
    print("\nStructured extraction:\n" + extracted.model_dump_json(indent=2))
    print("\nLayperson summary:\n" + summary)
