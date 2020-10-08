import graphene
from graphene_django import DjangoObjectType, DjangoListField
import bustracker.client as cta
from .models import Route, Pattern, Stop


class RoutesType(DjangoObjectType):
    class Meta:
        model = Route
        fields = ('number', 'name')


class VehicleType(graphene.ObjectType):
    number = graphene.String()
    pattern = graphene.String()
    destination = graphene.String()
    latitude = graphene.Float()
    longitude = graphene.Float()
    heading = graphene.Int()

    @classmethod
    def from_api_data(cls, data):
        ''' hydrate a VehicleType with data from the cta api '''
        return cls(
            number=data['vid'],
            pattern=data['pid'],
            destination=data['des'],
            latitude=data['lat'],
            longitude=data['lon'],
            heading=data['hdg'],
        )


class RouteType(DjangoObjectType):
    vehicles = graphene.List(VehicleType)

    def resolve_vehicles(self, info):
        return [VehicleType.from_api_data(x) for x in cta.get_vehicles(rt=self.number)]

    class Meta:
        model = Route
        fields = ('number', 'name', 'patterns')


class PatternType(DjangoObjectType):
    class Meta:
        model = Pattern
        fields = ('number', 'route', 'direction', 'stops')


class StopType(DjangoObjectType):
    class Meta:
        model = Stop
        fields = ('number', 'name', 'sequence', 'latitude', 'longitude')


class Query(graphene.ObjectType):
    routes = DjangoListField(RoutesType)
    route = graphene.Field(RouteType, number=graphene.String(required=True))

    def resolve_route(root, info, number):
        try:
            return Route.objects.get(number=number)
        except Route.DoesNotExist:
            return None


schema = graphene.Schema(query=Query)
