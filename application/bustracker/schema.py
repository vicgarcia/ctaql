import graphene
from graphene_django import DjangoObjectType
from .models import Route, Pattern, Stop


class ShallowRouteType(DjangoObjectType):
    class Meta:
        model = Route
        fields = ('number', 'name')


class RouteType(DjangoObjectType):
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
    routes = graphene.List(ShallowRouteType)
    route = graphene.Field(RouteType, number=graphene.String(required=True))

    def resolve_routes(root, info):
        return Route.objects.all()

    def resolve_route(root, info, number):
        try:
            return Route.objects.get(number=number)
        except Route.DoesNotExist:
            return None


schema = graphene.Schema(query=Query)
