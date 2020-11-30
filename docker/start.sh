#!/bin/sh

# change to application root
cd /code

# install dependencies
pipenv install --dev

# start dev server
pipenv run python application/debug.py runserver 0.0.0.0:8000
