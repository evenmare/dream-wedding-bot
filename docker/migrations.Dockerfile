FROM python:3.12

RUN python -m ensurepip --upgrade && \
    pip install uv

WORKDIR /app
COPY uv.lock pyproject.toml ./
COPY ./migrations ./migrations
COPY ./src ./src

RUN uv sync --locked --no-install-project --no-install-workspace

CMD [ "uv", "run", "aerich", "upgrade" ]
