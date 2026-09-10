"""Exercise 5: BaseTool with synchronous and asynchronous stock checks."""
import asyncio
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import BaseTool

load_dotenv(); model = ChatGroq(model="openai/gpt-oss-20b", api_key=os.getenv("GROQ_API_KEY"), temperature=0)

class StockCheckerTool(BaseTool):
    name: str = "check_product_stock"
    description: str = "Check whether a product ID is in stock."
    def _run(self, product_id: str) -> str:
        return "In stock" if product_id.upper() in {"P1023", "P2001"} else "Out of stock"
    async def _arun(self, product_id: str) -> str:
        await asyncio.sleep(0)
        return self._run(product_id)

stock_tool = StockCheckerTool()

def run(product_id, user_query):
    sync_result = stock_tool.invoke({"product_id": product_id})
    async_result = asyncio.run(stock_tool.ainvoke({"product_id": product_id}))
    bound = model.bind_tools([stock_tool]); first = bound.invoke(user_query)
    results = [ToolMessage(content=str(stock_tool.invoke(c["args"])), tool_call_id=c["id"]) for c in first.tool_calls]
    final = bound.invoke([HumanMessage(content=user_query), first, *results])
    return sync_result, async_result, first.tool_calls, [x.content for x in results], final.content

if __name__ == "__main__":
    product_id = input("Product ID: ").strip(); query = input("Question: ").strip()
    sync, async_value, calls, result, answer = run(product_id, query)
    print("Sync:", sync); print("Async:", async_value); print("Tool calls:", calls); print("Tool result:", result); print("Final answer:", answer)
