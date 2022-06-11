FROM python:3.9.13-slim-bullseye as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    POETRY_VERSION=1.1.5 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    \
    PYSETUP_PATH="/opt/pysetup"

ENV PATH="$POETRY_HOME/bin:$PATH"

FROM python-base as initial
RUN apt-get update \
    && apt-get install -y build-essential \
    && pip install -U pip poetry cmake

WORKDIR $PYSETUP_PATH

FROM initial as development-base
ENV POETRY_NO_INTERACTION=1
COPY poetry.lock pyproject.toml ./

FROM development-base as development
RUN poetry install

WORKDIR /app
