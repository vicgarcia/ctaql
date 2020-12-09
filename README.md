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

start the docker container

```
docker-compose up
```

use GraphiQL to interact at [http://0.0.0.0:8000/graphql/](http://0.0.0.0:8000/graphql/)

get list of all bus routes

```
{
  routes {
  	name
  	number
  }
}

output:

{
  "data": {
    "routes": [
      {
        "name": "Bronzeville/Union Station",
        "number": "1"
      },
      ...
      {
        "name": "Evanston Circulator",
        "number": "206"
      }
    ]
  }
}
```

get stops for a bus route

```
{
  route(number:"92") {
    number
    name
    stops {
      number
      name
      direction
      latitude
      longitude
    }
  }
}

output :

{
  "data": {
    "route": {
      "number": "92",
      "name": "Foster",
      "stops": [
        {
          "number": "4766",
          "name": "3700 W Foster",
          "direction": "Eastbound",
          "latitude": 41.975472,
          "longitude": -87.721260000001
        },
        ...
        {
          "number": "1041",
          "name": "Sheridan & Berwyn ",
          "direction": "Westbound",
          "latitude": 41.977888,
          "longitude": -87.655092
        }
      ]
    }
  }
}
```

get arrival times for a stop

```
{
  arrivals(stop:"1926") {
    route {
      number
      name
    }
    vehicle {
      number
      destination
    }
    direction
    time
  }
}

output :

{
  "data": {
    "arrivals": [
      {
        "route": {
          "number": "22",
          "name": "Clark"
        },
        "vehicle": {
          "number": "1873",
          "destination": "Howard"
        },
        "direction": "Northbound",
        "time": "20201208 22:30"
      }
    ]
  }
}
```

get a shell inside the running docker container

```
docker-compose exec ctaql-django-local sh
```

run manage.py inside the docker container

```
cd /code
pipenv run python manage.py <arguments here>
```
