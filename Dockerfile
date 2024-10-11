# --- Builder stage ---
FROM ghcr.io/astral-sh/uv:python3.12-bookworm AS builder

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    UV_COMPILE_BYTECODE=1

COPY ./pyproject.toml ./uv.lock ./

RUN uv sync --frozen --no-install-project

# --- Runtime stage ---
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY ./game.py /app/game.py

WORKDIR /app

CMD [ "uv", "run", "game.py" ]
