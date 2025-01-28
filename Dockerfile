FROM ghcr.io/astral-sh/uv:0.5.21 as uv


FROM python:3.12.8-bookworm

COPY --from=uv /uv /uvx /bin/

COPY pyproject.toml uv.lock src/app /app/

WORKDIR /app

RUN ["/bin/uv", "sync"]

ENTRYPOINT ["uv", "run", "fastapi", "run", "/app/app.py"]
