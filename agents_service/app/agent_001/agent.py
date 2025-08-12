import os

from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from app.agent_001.prompts.dev_prompt import get_dev_prompt
from app.agent_001.toolkit import get_toolkit
from app.core.config import settings
from app.agent_001.toolkit import example_tool


# Create the agent
def create_agent():
    # Initialize the LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=settings.openai_api_key,
    )

    # Create the ReAct agent
    agent = create_react_agent(
        model=llm,
        tools=[example_tool],
        prompt=get_dev_prompt(),
    )

    return agent
