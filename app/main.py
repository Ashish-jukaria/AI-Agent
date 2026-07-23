from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from app.graph import app_graph

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.post("/chat")
async def chat(request: ChatRequest):
    initial_state = {"messages": [HumanMessage(content=request.message)]}
    result = app_graph.invoke(initial_state)
    ai_response = result["messages"][-1].content
    return {"response": ai_response}