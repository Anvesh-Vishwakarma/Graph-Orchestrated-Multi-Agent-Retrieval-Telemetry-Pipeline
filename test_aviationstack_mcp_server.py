import os 
import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")

client = MultiServerMCPClient(
        {
            "aviationstack": {
                "transport": "stdio",
                "command": r"F:\AI Travel Planner RAG Systen\aviationstack-mcp\.venv\Scripts\python.exe",
                "args": [
                    "-m",
                    "aviationstack_mcp",
                    "mcp",
                    "run"
                ],
                "env": {
                    "AVIATIONSTACK_API_KEY": AVIATIONSTACK_API_KEY
                }
            }
        }
    )

async def main():
    tools = await client.get_tools()

    print("\nAvailable Tools\n")

    for tool in tools:
        print(tool.name)

if __name__ == "__main__":
    asyncio.run(main())