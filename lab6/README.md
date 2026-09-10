# Lab 6 - Tools and Tool Calling

Each exercise is a standalone Python script using `ChatGroq`, `bind_tools()`, and manual execution of the model's suggested tool calls. Set `GROQ_API_KEY` in the root `.env` file and run a script from the repository root:

```powershell
python lab6/exercise1_order_status.py
```

Exercises use small mock data stores so no additional APIs are required. Exercise 5 demonstrates both `.invoke()` and `.ainvoke()` on a `BaseTool` subclass.
