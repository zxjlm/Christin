ARG PYTHON_VERSION="3.8.5"
ARG NODE_VERSION="15.3.0"
FROM node:${NODE_VERSION}-alpine AS frontend-builder

COPY frontend/ /frontend/
WORKDIR /frontend

# hadolint ignore=DL3018
RUN apk add -U --no-cache git python3 make g++ \
    && yarn install \
    && yarn build \
    && apk del --no-cache git make g++

FROM python:${PYTHON_VERSION}-slim-buster AS backend-builder

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    netcat=1.* \
    libpq-dev=11.* \
    unixodbc-dev=2.* \
    g++=4:* \
    libssl-dev=1.* \
    && apt-get clean

WORKDIR /tmp
COPY Pipfile* /tmp/

# hadolint ignore=DL3013
RUN pip install --no-cache-dir -U pip pipenv==2020.11.15 \
    && pipenv lock -r > /requirements.txt \
    && echo "psycopg2-binary==2.8.6" >> /requirements.txt \
    && echo "django-heroku==0.3.1" >> /requirements.txt \
    && pip install --no-cache-dir -r /requirements.txt \
    && pip wheel --no-cache-dir -r /requirements.txt -w /deps
