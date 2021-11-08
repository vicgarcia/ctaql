ctaql is an experiment with [GraphQL](https://graphql.org/) to provide access to the [CTA Bus Tracker API](https://www.transitchicago.com/developers/bustracker/)

see it in action at [https://ctaql.cc](https://ctaql.cc/#query=%7B%0A%20%20route(number%3A%20%2274%22)%20%7B%0A%20%20%20%20number%0A%20%20%20%20name%0A%20%20%20%20vehicles%20%7B%0A%20%20%20%20%20%20number%0A%20%20%20%20%20%20destination%0A%20%20%20%20%20%20heading%0A%20%20%20%20%20%20latitude%0A%20%20%20%20%20%20longitude%0A%20%20%20%20%7D%20%20%20%20%0A%20%20%20%20directions%20%7B%0A%20%20%20%20%20%20direction%0A%20%20%20%20%7D%0A%20%20%20%20stops%20%7B%0A%20%20%20%20%20%20number%0A%20%20%20%20%20%20name%0A%20%20%20%20%20%20latitude%0A%20%20%20%20%20%20longitude%0A%20%20%20%20%20%20direction%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D)

<br>

get list of all bus routes
```
query:

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
query:

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
query:

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

<br />

clone the repository
```
git clone git@github.com:vicgarcia/ctaql.git
cd ctaql
```

copy the .env file from the example and add SECRET_KEY and CTA_BUSTRACKER_API_KEY
```
cp .env.example .env
vim .env
```

build + start the docker container
```
docker-compose build
docker-compose up
```

use GraphiQL to interact at [http://0.0.0.0:8000/graphql/](http://0.0.0.0:8000/graphql/)

get a shell inside the running docker container
```
docker-compose exec ctaql-django-local sh
```

run manage.py inside the docker container
```
cd /code
pipenv run python manage.py <arguments here>
```
