FROM python:3.9 AS base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install -U pip && pip install pipenv


FROM base AS dev

RUN echo $'#!/bin/sh\n\
cd /code\n\
pipenv install --dev\n\
pipenv run python ctaql/debug.py runserver 0.0.0.0:8000\n\
' > /start.sh && chmod 777 /start.sh


FROM base AS build

ENV PIPENV_VENV_IN_PROJECT 1

RUN pip install pipenv
RUN mkdir -p /code
COPY . /code
WORKDIR /code

RUN pipenv install


FROM build AS test

ENV PIPENV_VENV_IN_PROJECT 1

RUN pipenv install --dev

# CMD [ "/code/.venv/bin/pytest" ]


FROM build AS prod

RUN echo $'#!/bin/sh\n\
cd /code\n\
pipenv run gunicorn ctaql.wsgi --bind 0.0.0.0:8000\n\
' > /start.sh && chmod 777 /start.sh

# CMD [ "/start.sh" ]
