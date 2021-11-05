FROM python:3.9 AS base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install -U pip


FROM base AS development

RUN pip install pipenv

RUN echo '#!/bin/sh\n\
cd /code\n\
pipenv install --dev\n\
pipenv run python ctaql/debug.py runserver 0.0.0.0:8000\n\
' > /start.sh && chmod +x /start.sh

CMD [ "/start.sh" ]


FROM base AS build

ENV PIPENV_VENV_IN_PROJECT 1

ENV DJANGO_CONFIGURATION production
ENV DJANGO_SETTINGS_MODULE settings

RUN pip install pipenv

RUN mkdir -p /code
COPY . /code

WORKDIR /code

RUN pipenv install

RUN pipenv run python ctaql/manage.py collectstatic --noinput


FROM build AS test

ENV DJANGO_CONFIGURATION test

RUN pipenv install --dev


FROM base AS production

ENV DJANGO_CONFIGURATION production

COPY --from=build /code /code

WORKDIR /code/ctaql

CMD [ "/code/.venv/bin/gunicorn", "wsgi", "--bind", "0.0.0.0:8000" ]
