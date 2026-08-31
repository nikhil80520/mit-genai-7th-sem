# Lab 5 - Workflow Design with LLMs

This folder contains all six Lab 5 exercises. Each pipeline uses the required LangChain components:

- `PromptTemplate` plus `PydanticOutputParser` for raw-text extraction.
- `ChatPromptTemplate` plus `StrOutputParser` for free-form generation.
- `ChatPromptTemplate` plus `PydanticOutputParser` for evaluation and final structured output.

Each exercise is fully standalone, matching the Lab 4 format: it has its own dotenv/Groq setup, prompts, functions, and interactive runner. The scripts format their LangChain prompts, call the Groq SDK directly, then parse each response with the required output parser. Set `GROQ_API_KEY` in the root `.env` file, then run scripts from this folder or from the repository root:

```powershell
python lab5/exercise1_review_support_ticket.py
```

The later stages receive serialized parsed Pydantic data only, never the original raw input.
