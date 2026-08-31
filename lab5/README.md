# Lab 5 - Workflow Design with LLMs

This folder contains all six Lab 5 exercises. Each pipeline uses the required LangChain components:

- `PromptTemplate` plus `PydanticOutputParser` for raw-text extraction.
- `ChatPromptTemplate` plus `StrOutputParser` for free-form generation.
- `ChatPromptTemplate` plus `PydanticOutputParser` for evaluation and final structured output.

Each exercise is fully standalone, matching the Lab 4 format: it has its own dotenv setup, prompts, functions, and interactive runner. It uses `ChatGroq` with the standard flow: `prompt.invoke(...)`, then `model.invoke(prompt)`, then `parser.invoke(result)`. Install `langchain-groq` before running the scripts, set `GROQ_API_KEY` in the root `.env` file, then run scripts from this folder or from the repository root:

```powershell
python lab5/exercise1_review_support_ticket.py
```

The later stages receive serialized parsed Pydantic data only, never the original raw input.
