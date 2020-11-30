import graphene
from graphql import GraphQLError
from graphene_django import DjangoObjectType, DjangoListField
from .functions import (
    get_routes,
    get_directions_by_route,
    get_stops_by_route_and_direction,
    get_predictions_by_route_and_stop,
    get_predictions_by_vehicle,
    get_vehicles_by_route,
)


class VehicleType(graphene.ObjectType):
    number = graphene.String()
    destination = graphene.String()
    latitude = graphene.Float()
    longitude = graphene.Float()
    heading = graphene.Int()

    @classmethod
    def from_api_data(cls, data):
        ''' hydrate a VehicleType with data from the cta api '''
        return cls(
            number=data['vid'],
            destination=data['des'],
            latitude=data['lat'],
            longitude=data['lon'],
            heading=data['hdg'],
        )


class DirectionType(graphene.ObjectType):
    direction = graphene.String()

    @classmethod
    def from_api_data(cls, data):
        ''' hydrate a DirectionType with data from the cta api '''
        return cls(
            direction=data['dir'],
        )


class StopType(graphene.ObjectType):
    number = graphene.String()
    name = graphene.String()
    direction = graphene.String()
    latitude = graphene.Float()
    longitude = graphene.Float()

    @classmethod
    def from_api_data(cls, direction, data):
        ''' hydrate a StopType with data from cta api '''
        return cls(
            number=data['stpid'],
            name=data['stpnm'],
            direction=direction,
            latitude=data['lat'],
            longitude=data['lon'],
        )


class RouteType(graphene.ObjectType):
    number = graphene.String()
    name = graphene.String()
    directions = graphene.List(DirectionType)
    stops = graphene.List(StopType, direction=graphene.String(required=False))
    vehicles = graphene.List(VehicleType)

    def resolve_directions(root, info):
        directions = get_directions_by_route(root.number)
        return [DirectionType.from_api_data(d) for d in directions]

    def resolve_stops(root, info, direction=None):
        directions = get_directions_by_route(root.number)
        stops = []
        for direction in [d['dir'] for d in directions]:
            direction_stops = get_stops_by_route_and_direction(root.number, direction)
            stops.extend([StopType.from_api_data(direction, s) for s in direction_stops])
        return stops

    def resolve_vehicles(root, info):
        vehicles = get_vehicles_by_route(root.number)
        return [VehicleType.from_api_data(v) for v in vehicles]

    @classmethod
    def from_api_data(cls, data):
        return cls(
            number=data['rt'],
            name=data['rtnm'],
        )


class RoutesType(graphene.ObjectType):
    number = graphene.String()
    name = graphene.String()

    @classmethod
    def from_api_data(cls, data):
        ''' hydrate from cta bustracker /getroutes data '''
        return cls(
            number=data['rt'],
            name=data['rtnm'],
        )


class PredictionRouteType(RoutesType):

    @classmethod
    def from_route_number(cls, number):
        routes = { r['rt']: r for r in get_routes() }
        route = routes[number]
        return cls.from_api_data(route)


class PredictionStopType(graphene.ObjectType):
    number = graphene.String()
    name = graphene.String()

    @classmethod
    def from_api_data(cls, data):
        return cls(
            number=data['stpid'],
            name=data['stpnm'],
        )


class PredictionVehicleType(graphene.ObjectType):
    number = graphene.String()
    destination = graphene.String()

    @classmethod
    def from_api_data(cls, data):
        return cls(
            number=data['vid'],
            destination=data['des'],
        )


class PredictionType(graphene.ObjectType):
    route = graphene.Field(PredictionRouteType)
    stop = graphene.Field(PredictionStopType)
    vehicle = graphene.Field(PredictionVehicleType)
    direction = graphene.String()
    time = graphene.String()

    @classmethod
    def from_api_data(cls, data):
        return cls(
            route=PredictionRouteType.from_route_number(data['rt']),
            stop=PredictionStopType.from_api_data(data),
            vehicle=PredictionVehicleType.from_api_data(data),
            direction=data['rtdir'],
            time=data['prdtm'],
        )


class Query(graphene.ObjectType):
    routes = graphene.List(RoutesType)
    route = graphene.Field(RouteType, number=graphene.String(required=True))
    predictions = graphene.List(PredictionType,
        vehicle=graphene.String(required=False),
        route=graphene.String(required=False),
        stop=graphene.String(required=False),
    )

    def resolve_routes(root, info):
        routes = get_routes()
        return [RoutesType.from_api_data(r) for r in routes]

    def resolve_route(root, info, number):
        routes = { r['rt']: r for r in get_routes() }
        route = routes[number]
        # todo: error handling here
        return RouteType.from_api_data(route)

    def resolve_predictions(root, info, vehicle=None, route=None, stop=None):
        # todo: error handle + param mixing
        predictions = []
        if vehicle is not None:
            predictions = get_predictions_by_vehicle(vehicle)
        else:
            predictions = get_predictions_by_route_and_stop(route, stop)
        return [PredictionType.from_api_data(p) for p in predictions]


schema = graphene.Schema(query=Query)
