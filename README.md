ctaql is an experiment with using GraphQL to provide access to data from the [CTA bustracker api](https://www.transitchicago.com/developers/bustracker/)

### getting started

clone the repositry
```
    git clone git@github.com:vicgarcia/ctaql.git
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
