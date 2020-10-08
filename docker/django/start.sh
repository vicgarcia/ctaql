#!/bin/sh

# change to application root
cd /code

# install dependencies
pipenv install --dev

# wait for postgres container to start
while ! nc -z ctaql-postgres-local 5432; do
    echo "postgres is unavailable. waiting ..." && sleep 20
done
echo "postgres is up" && sleep 10

# run migrations
pipenv run python application/manage.py migrate

# start dev server
pipenv run python application/debug.py runserver 0.0.0.0:8000
