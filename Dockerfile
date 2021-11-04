FROM python:3.9-alpine AS base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add python3-dev
RUN pip install -U pip && pip install pipenv


FROM base AS development

RUN echo $'#!/bin/sh\n\
cd /code\n\
pipenv install --dev\n\
pipenv run python ctaql/debug.py runserver 0.0.0.0:8000\n\
' > /start.sh && chmod 777 /start.sh


FROM base AS build

RUN mkdir -p /code
COPY .. /code
WORKDIR /code


FROM build AS test

RUN pipenv install --dev


FROM build AS production

RUN pipenv install

RUN echo $'#!/bin/sh\n\
cd /code\n\
pipenv run gunicorn ctaql.wsgi --bind 0.0.0.0:8000\n\
' > /start.sh && chmod 777 /start.sh

CMD [ "/start.sh" ]
