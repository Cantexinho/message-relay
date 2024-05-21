FROM python:3.12-slim-bookworm
LABEL maintainer="PK"

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

COPY message_sender_api ./message_sender_api

EXPOSE 8001

CMD ["poetry", "run", "uvicorn", "message_sender_api.main:app", "--host", "0.0.0.0", "--port", "8001"]