FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY .python-version pyproject.toml uv.lock /code/
RUN uv sync --frozen --no-cache

COPY ./src /code/app

HEALTHCHECK --interval=30s --timeout=1s CMD curl --fail http://localhost:8080/health || exit 1
EXPOSE 8080/tcp

CMD [".venv/bin/fastapi", "run", "app/main.py", "--port", "8080", "--host", "0.0.0.0"]
