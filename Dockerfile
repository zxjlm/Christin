ARG PYTHON_VERSION="3.8.5"
ARG NODE_VERSION="15.3.9"
FROM node:${NODE_VERSION}-alpine AS frontend-builder

COPY frontend/ /app/
WORKDIR /app

RUN apk add -U --no-cache git python3 make g++ \
    && npm install -g yarn \
    && yarn install \
    && yarn build \
    && apk del --no-cache git make g++
# pull official base image
FROM python:${PYTHON_VERSION}

WORKDIR /Christin
USER root

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.1.4

# install dependencies
RUN pip install "poetry==$POETRY_VERSION"
COPY ./backend/poetry.lock ./backend/pyproject.toml /Christin/
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# copy project
COPY ./backend/ /Christin/

ENV DATABASE_URL="sqlite:////data/doccano.db"

ENV DEBUG="True"
ENV SECRET_KEY="change-me-in-production"
ENV PORT="8000"
ENV WORKERS="2"
ENV CELERY_WORKERS="2"

VOLUME /data
EXPOSE ${PORT}

CMD ["flask", "run"]