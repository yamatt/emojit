FROM ghcr.io/astral-sh/uv:0.5.21 as uv


FROM gcr.io/distroless/python3-debian12:latest

COPY --from=uv /uv /uvx /bin/

RUN /bin/uv sync

ENTRYPOINT ["/horust", "--services-path", "/services"]
