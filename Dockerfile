FROM python:3.12-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY . /code

# Install the application dependencies.
WORKDIR /code
RUN uv sync --frozen --no-cache

HEALTHCHECK --interval=30s --timeout=1s CMD curl --fail http://localhost:8080/health || exit 1
EXPOSE 8080/tcp
# Run the application.
CMD ["/app/.venv/bin/fastapi", "run", "app/main.py", "--port", "8080", "--host", "0.0.0.0"]