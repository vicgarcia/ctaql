ctaql is an experiment with using GraphQL to provide access to data from the [CTA bustracker api](https://www.transitchicago.com/developers/bustracker/). it uses django to provide a graphql api, with the data being retrieve and cached from the CTA's REST api.

clone the repositry

```
git clone git@github.com:vicgarcia/ctaql.git
cd ctaql
```

copy the .env file from the example and add SECRET_KEY and CTA_BUSTRACKER_API_KEY

```
cp .env.example .env
vim .env
```

build the docker container

```
docker-compose build --no-cache
```

start the docker containers

```
docker-compose up
```

use [Insomnia](https://insomnia.rest/) to make API calls with the insomnia.yaml file

get a shell inside the running docker container

```
docker-compose exec ctaql-django-local sh
```

run manage.py inside the docker container

```
cd /code
pipenv run python manage.py <arguments here>
```
