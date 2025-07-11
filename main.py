import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from sse_starlette import EventSourceResponse

from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

from src.database import init_db
from src.api import register_route

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    register_route(app)
    print("====== applicaiton start ======")
    yield
    print("====== applicaiton shutdown ======")


app = FastAPI(lifespan=lifespan)


model = ChatOllama(
    model="deepseek-r1:1.5b",
    base_url="http://112.125.89.224:11434",
)

agent = create_react_agent(model=model, tools=[], prompt="You are a helpful assistant")


@app.post("/stream")
async def stream_endpoint(request: Request):
    async def event_generator():
        # 使用正确的流式调用
        async for chunk in agent.astream(
            input={"messages": [{"role": "user", "content": "Who are you?"}]},
            stream_mode="messages",
        ):
            # 添加超时检查
            if await request.is_disconnected():
                break

            # 格式化 SSE 响应
            yield {"event": "message", "data": chunk[0].content}

            # 添加延迟防止过载
            await asyncio.sleep(0.05)

    return EventSourceResponse(event_generator())


