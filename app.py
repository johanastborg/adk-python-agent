import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import ParticlePhysicsAgent

app = FastAPI(title="Particle Physics Agent")

# Initialize agent
try:
    # On Cloud Run, env vars are set in the service configuration
    # locally, we might rely on python-dotenv loaded in agent.py or here
    agent = ParticlePhysicsAgent()
except Exception as e:
    print(f"Failed to initialize agent: {e}")
    agent = None

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.get("/")
def health_check():
    return {"status": "ok", "agent_initialized": agent is not None}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    try:
        # The agent.ask method abstracts the underlying ADK complexity
        response_text = agent.ask(request.message)
        return ChatResponse(response=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
