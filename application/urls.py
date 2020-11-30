from django.urls import path
from graphene_django.views import GraphQLView
from health import HealthCheckView
from bustracker.schema import schema


urlpatterns = [

    # health check endpoint
    path('health/', HealthCheckView.as_view()),

    # graphql endpoint
    path ('graphql/', GraphQLView.as_view(graphiql=True, schema=schema))

]
