from fastapi import FastAPI
from app.agent_001.agent import create_agent
from app.orchestrator.models import AgentRequest

app = FastAPI()
agent = create_agent()


@app.post("/chat")
async def root(request: AgentRequest):
    r = request
    q = request.message
    print(q)
    result = await agent.ainvoke(
        {
            "messages": [
                {"role": "user", "content": request.message},
            ]
        }
    )
    print(len(result["messages"]))
    ai_message = result["messages"][-1].content
    return {"message": ai_message}
