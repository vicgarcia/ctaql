FROM python:3.8-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# os library dependencies
RUN apk update && apk add python3-dev

# update pip and install pipenv
RUN pip install -U pip && pip install pipenv

# setup path for codebase
RUN mkdir -p /code
WORKDIR /code

# copy pipfile and install dependencies
COPY Pipfile* /code/
RUN pipenv install --dev
