FROM python:3.9 AS base

RUN pip install -U pip


FROM base AS development

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install pipenv

RUN echo '#!/bin/sh\n\
cd /code\n\
pipenv install --dev\n\
pipenv run python ctaql/debug.py runserver 0.0.0.0:8000\n\
' > /start.sh && chmod +x /start.sh

CMD [ "/start.sh" ]


FROM base AS build

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV PIPENV_VENV_IN_PROJECT 1
ENV PIPENV_COLORBLIND 1
ENV PIPENV_NOSPIN 1

ENV DJANGO_SETTINGS_MODULE settings
ENV DJANGO_CONFIGURATION base

RUN pip install pipenv

RUN mkdir -p /code
COPY . /code

WORKDIR /code

RUN pipenv install

RUN pipenv run python ctaql/manage.py collectstatic --noinput


FROM build AS test

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV PIPENV_VENV_IN_PROJECT 1
ENV PIPENV_COLORBLIND 1
ENV PIPENV_NOSPIN 1

ENV DJANGO_SETTINGS_MODULE settings
ENV DJANGO_CONFIGURATION base

RUN pipenv install --dev


FROM base AS production

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV DJANGO_SETTINGS_MODULE settings
ENV DJANGO_CONFIGURATION production

COPY --from=build /code /code

WORKDIR /code/ctaql

CMD [ "/code/.venv/bin/gunicorn", "wsgi", "--bind", "0.0.0.0:8000" ]
