"""Exercise 4: Generate a consistent, word-limited customer-support reply."""
import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY is missing from .env")
client = Groq(api_key=api_key)


SYSTEM_PROMPT = """You write customer-support replies for the named company.
Be empathetic, calm, concise, and professional. Acknowledge the customer's
issue, state the next useful action, and do not promise anything unsupported.
Output format: return only the complete reply text, with no subject line,
labels, analysis, quotation marks, or extra commentary."""


def build_prompt(customer_message, company_name, max_words):
    return f"""Company: {company_name}
Customer message: {customer_message}
Maximum words: {max_words}

Write a complete reply using no more than {max_words} words."""


def support_reply(customer_message, company_name, max_words):
    if max_words < 1:
        raise ValueError("max_words must be positive.")
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        temperature=0.3,
        max_tokens=max(300, max_words * 3),
        reasoning_effort="low",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_prompt(customer_message, company_name, max_words)},
        ],
    )
    reply = response.choices[0].message.content.strip()
    if len(reply.split()) > max_words:
        raise ValueError("The generated reply exceeded the word limit.")
    return reply


if __name__ == "__main__":
    message = input("Customer message: ").strip()
    company = input("Company name: ").strip()
    limit = int(input("Maximum words: ").strip())
    print(support_reply(message, company, limit))