import uvicorn
from fastapi import FastAPI

from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

app = FastAPI()

model = ChatOllama(
    model="deepseek-r1:1.5b",
    base_url="http://112.125.89.224:11434",
)

agent = create_react_agent(
    model=model,
    tools=[],
    prompt="You are a helpful assistant"  
)


@app.post("/")
async def read_root():
    return await agent.ainvoke(
        {"messages": [{"role": "user", "content": "Who are you"}]}
    )