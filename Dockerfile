FROM ghcr.io/astral-sh/uv:python3.12-alpine

COPY . /app

WORKDIR /app

RUN uv sync --locked

RUN source .venv/bin/activate

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "40000", "--timeout-keep-alive", "20"]
