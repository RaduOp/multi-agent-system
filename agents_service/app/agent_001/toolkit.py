from langchain_core.runnables.config import RunnableConfig
from langchain.tools import tool
from typing import Dict, Any


@tool(parse_docstring=True)
async def example_tool(query: str, config: RunnableConfig) -> Dict[str, Any]:
    """
    Mocked async example tool.

    Args:
        query (str): A query that summarizes the user's message
        config (RunnableConfig): A RunnableConfig instance, will be automatically passed.

    Returns:
        Dict[str, Any]: Mocked API-like response.
    """

    # Replace with your actual async HTTP call when ready:
    # async with httpx.AsyncClient() as client:
    #     resp = await client.post("http://tools-service:8000/feature_1", json={...})
    #     return resp.json()

    # Mocked response instead
    return {
        "status": "success",
        "data": {
            "query": query,
            "response": "This is a mocked async response from tools-service, "
            "meaning the async tool call works.",
        },
    }


def get_toolkit():
    return [example_tool]
