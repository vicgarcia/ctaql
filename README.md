ctaql is an experiment with [GraphQL](https://graphql.org/) to provide access to the [CTA Bus Tracker API](https://www.transitchicago.com/developers/bustracker/). [Graphene-Django](https://docs.graphene-python.org/projects/django/en/latest/) is used to define a schema that describes the data and implement the query logic to retrieve the [bustracker](https://github.com/vicgarcia/bustracker) data.

### see it in action at [https://ctaql.rockst4r.net](https://ctaql.rockst4r.net/#query=%7B%0A%20%20route(number%3A%20%22151%22)%20%7B%0A%20%20%20%20number%0A%20%20%20%20name%0A%20%20%20%20vehicles%20%7B%0A%20%20%20%20%20%20number%0A%20%20%20%20%20%20destination%0A%20%20%20%20%20%20heading%0A%20%20%20%20%20%20latitude%0A%20%20%20%20%20%20longitude%0A%20%20%20%20%7D%20%20%20%20%0A%20%20%20%20directions%20%7B%0A%20%20%20%20%20%20direction%0A%20%20%20%20%7D%0A%20%20%20%20stops%20%7B%0A%20%20%20%20%20%20number%0A%20%20%20%20%20%20name%0A%20%20%20%20%20%20latitude%0A%20%20%20%20%20%20longitude%0A%20%20%20%20%20%20direction%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D)

try running these queries

**get list of all bus routes**
```
{
  routes {
    name
    number
  }
}
```

output
```
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

**get stops for a bus route**
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
```

output
```
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

**get arrival times for a stop**
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
```

output
```
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

**get vehicles on a route**
```
{
  route(number: "151") {
    vehicles {
      number
      destination
      heading
      latitude
      longitude
    }
  }
}
```

output
```
{
  "data": {
    "route": {
      "vehicles": [
        {
          "number": "4166",
          "destination": "Foster",
          "heading": 359,
          "latitude": 41.93389840853416,
          "longitude": -87.63931662349377
        },
        ...
        {
          "number": "4358",
          "destination": "Union Station",
          "heading": 280,
          "latitude": 41.87939778312308,
          "longitude": -87.6361819407979
        }
      ]
    }
  }
}
```

**get predictions for a vehicle**
```
{
  arrivals(vehicle: "1819") {
    stop {
      number
      name
    }
    direction
    time
  }
}
```

output
```
{
  "data": {
    "arrivals": [
      {
        "stop": {
          "number": "14176",
          "name": "Clark & Arthur Terminal"
        },
        "direction": "Southbound",
        "time": "20211109 20:48"
      },
      ...
      {
        "stop": {
          "number": "1039",
          "name": "Sheridan & Catalpa"
        },
        "direction": "Southbound",
        "time": "20211109 21:00"
      }
    ]
  }
}
```

<br />

### development

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
