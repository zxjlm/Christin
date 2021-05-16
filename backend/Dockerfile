# pull official base image
FROM python:3.7

MAINTAINER harumonia
WORKDIR /Poirot
USER root

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip -i https://pypi.douban.com/simple
COPY ./requirements.txt .
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple
RUN pip install flask_mail -i https://pypi.douban.com/simple

# copy project
COPY . .
