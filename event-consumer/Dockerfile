FROM python:3.12-slim-bookworm
LABEL maintainer="PK"

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

COPY event_consumer ./event_consumer

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "event_consumer.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]