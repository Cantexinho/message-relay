FROM python:3.12-slim-bookworm
LABEL maintainer="PK"

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

COPY event_propagator ./event_propagator

EXPOSE 8001

CMD ["poetry", "run", "python", "event_propagator/main.py"]