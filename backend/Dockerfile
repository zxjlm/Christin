# pull official base image
FROM python:3.8.5

LABEL maintainer="harumonia"    
WORKDIR /Christin
USER root

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.1.4

# install dependencies
RUN pip install "poetry==$POETRY_VERSION"
COPY ./backend/ /Christin/
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# copy project
# COPY . .
