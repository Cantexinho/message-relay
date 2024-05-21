FROM python:3.12-slim-bookworm
LABEL maintainer="PK"

ENV PYTHONUNBUFFERED 1

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /app/

COPY ./message_sender_api /app
WORKDIR /app

EXPOSE 8001

RUN poetry install --no-root && \
    adduser \
        --disabled-password \
        --no-create-home \
        api-user

RUN mkdir /py && cp -r $(poetry env info --path)/* /py

ENV PATH="/py/bin:$PATH"

USER api-user