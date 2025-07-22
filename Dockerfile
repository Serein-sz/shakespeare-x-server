FROM ghcr.io/astral-sh/uv:python3.12-alpine

COPY . /app

WORKDIR /app

RUN source .venv/bin/activate

RUN uv sync --locked

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--timeout-keep-alive", "300"]
