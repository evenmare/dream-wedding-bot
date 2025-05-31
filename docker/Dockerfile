FROM python:3.13

RUN python -m ensurepip --upgrade && \
    pip install uv

WORKDIR /app
COPY uv.lock pyproject.toml ./
COPY ./migrations ./migrations
COPY ./src ./src

RUN uv sync --locked --no-install-project --no-install-workspace
RUN uv pip list

WORKDIR /app/src

CMD [ "uv", "run", "__main__.py" ]
