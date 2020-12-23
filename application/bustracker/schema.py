import graphene
from graphql import GraphQLError
from graphene_django import DjangoObjectType, DjangoListField
from .cached import (
    get_routes,
    get_directions_by_route,
    get_stops_by_route_and_direction,
    get_predictions_by_vehicle,
    get_predictions_by_stop,
    get_vehicles_by_route,
)


class RoutesType(graphene.ObjectType):
    number = graphene.String(description="route number")
    name = graphene.String(description="route name")

    @classmethod
    def from_api_data(cls, data):
        return cls(
            number=data['rt'],
            name=data['rtnm'],
        )

    class Meta:
        description = 'bus route'


class RouteDirectionType(graphene.ObjectType):
    direction = graphene.String(description="route direction")

    @classmethod
    def from_api_data(cls, data):
        return cls(
            direction=data['dir'],
        )

    class Meta:
        description = 'direction of travel'


class RouteStopType(graphene.ObjectType):
    number = graphene.String(description="stop number")
    name = graphene.String(description="stop name")
    direction = graphene.String(description="stop direction")
    latitude = graphene.Float(description="stop location latitude")
    longitude = graphene.Float(description="stop location longitude")

    @classmethod
    def from_api_data(cls, direction, data):
        return cls(
            number=data['stpid'],
            name=data['stpnm'],
            direction=direction,
            latitude=data['lat'],
            longitude=data['lon'],
        )

    class Meta:
        description = 'bus stop'


class RouteVehicleType(graphene.ObjectType):
    number = graphene.String(description="vehicle number")
    destination = graphene.String(description="vehicle destination")
    latitude = graphene.Float(description="vehicle position latitude")
    longitude = graphene.Float(description="vehicle position longitude")
    heading = graphene.Int(description="vehicle position heading")

    @classmethod
    def from_api_data(cls, data):
        return cls(
            number=data['vid'],
            destination=data['des'],
            latitude=data['lat'],
            longitude=data['lon'],
            heading=data['hdg'],
        )

    class Meta:
        description = 'bus vehicle'


class RouteType(RoutesType):
    directions = graphene.List(RouteDirectionType,
        description="route directions",
    )
    stops = graphene.List(RouteStopType,
        direction=graphene.String(required=False),
        description="route stops",
    )
    vehicles = graphene.List(RouteVehicleType,
        description="route vehicles",
    )

    def resolve_directions(root, info):
        directions = get_directions_by_route(root.number)
        return [RouteDirectionType.from_api_data(d) for d in directions]

    def resolve_stops(root, info, direction=None):
        directions = get_directions_by_route(root.number)
        stops = []
        for direction in [d['dir'] for d in directions]:
            direction_stops = get_stops_by_route_and_direction(root.number, direction)
            stops.extend([RouteStopType.from_api_data(direction, s) for s in direction_stops])
        return stops

    def resolve_vehicles(root, info):
        vehicles = get_vehicles_by_route(root.number)
        return [RouteVehicleType.from_api_data(v) for v in vehicles]

    class Meta:
        description = 'bus route'


class ArrivalsRouteType(RoutesType):

    @classmethod
    def from_route_number(cls, number):
        routes = { r['rt']: r for r in get_routes() }
        route = routes[number]
        return cls.from_api_data(route)

    class Meta:
        description = 'bus route'


class ArrivalsRouteStopType(graphene.ObjectType):
    number = graphene.String(description="stop number")
    name = graphene.String(description="stop name")

    @classmethod
    def from_api_data(cls, data):
        return cls(
            number=data['stpid'],
            name=data['stpnm'],
        )

    class Meta:
        description = 'bus stop'


class ArrivalsRouteVehicleType(graphene.ObjectType):
    number = graphene.String(description="vehicle number")
    destination = graphene.String(description="vehicle destination")


    @classmethod
    def from_api_data(cls, data):
        return cls(
            number=data['vid'],
            destination=data['des'],
        )

    class Meta:
        description = 'bus vehicle'


class ArrivalsType(graphene.ObjectType):
    route = graphene.Field(ArrivalsRouteType, description="bus route")
    stop = graphene.Field(ArrivalsRouteStopType, description="bus stop")
    vehicle = graphene.Field(ArrivalsRouteVehicleType, description="bus vehicle")
    direction = graphene.String(description="travel direction")
    time = graphene.String(description="arrival time")

    @classmethod
    def from_api_data(cls, data):
        return cls(
            route=ArrivalsRouteType.from_route_number(data['rt']),
            stop=ArrivalsRouteStopType.from_api_data(data),
            vehicle=ArrivalsRouteVehicleType.from_api_data(data),
            direction=data['rtdir'],
            time=data['prdtm'],
        )

    class Meta:
        description = 'arrival times'


class Query(graphene.ObjectType):
    routes = graphene.List(RoutesType,
        description="list all bus routes",
    )

    route = graphene.Field(RouteType,
        description="bus route by number",
        number=graphene.String(description="route number", required=True),
    )

    arrivals = graphene.List(ArrivalsType,
        description="arrival times by vehicle or stop",
        vehicle=graphene.String(description="vehicle number", required=False),
        stop=graphene.String(description="stop number", required=False),
    )

    def resolve_routes(root, info):
        routes = get_routes()
        return [RoutesType.from_api_data(r) for r in routes]

    def resolve_route(root, info, number):
        routes = { r['rt']: r for r in get_routes() }
        route = routes[number]
        # todo: error handling here
        return RouteType.from_api_data(route)

    def resolve_arrivals(root, info, vehicle=None, stop=None):
        arrivals = []
        if vehicle is not None:
            arrivals = get_predictions_by_vehicle(vehicle)
        else:
            arrivals = get_predictions_by_stop(stop)
        # todo: error handle here
        return [ArrivalsType.from_api_data(p) for p in arrivals]

    class Meta:
        description = 'cta bustracker'


schema = graphene.Schema(query=Query)
