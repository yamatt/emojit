FROM ghcr.io/astral-sh/uv:0.5.21 as uv


FROM gcr.io/distroless/python3-debian12:latest

COPY --from=uv /uv /uvx /bin/

ADD pyproject.toml uv.lock src/app /app/

WORKDIR /app

SHELL ["busybox", "sh", "-c"]
RUN ["/bin/uv", "sync"]

ENTRYPOINT ["python3", "-m", "fastapi", "run", "/app/src/app/app.py"]
