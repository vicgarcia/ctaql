from graphene_django.views import GraphQLView
from rest_framework.request import Request
from users.authentication import JSONWebTokenAuthentication, IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes, api_view


class AuthenticatedGraphQLView(GraphQLView):

    def parse_body(self, request):
        if isinstance(request, Request):
            return request.data
        return super(AuthenticatedGraphQLView, self).parse_body(request)

    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super(AuthenticatedGraphQLView, cls).as_view(*args, **kwargs)
        view = permission_classes((IsAuthenticated,))(view)
        view = authentication_classes((JSONWebTokenAuthentication,))(view)
        view = api_view(['GET', 'POST'])(view)
        return view


# https://github.com/graphql-python/graphene/issues/249
