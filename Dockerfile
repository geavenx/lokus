FROM python:3.12-slim-bookworm

# Copy uv bin
COPY --from=ghcr.io/astral-sh/uv:0.7.8 /uv /uvx /bin/

WORKDIR /app

# Copy app code
COPY . .

# Install deps
RUN uv sync --locked --no-dev


ENTRYPOINT ["uv", "run", "-q", "swagger-validator"]
