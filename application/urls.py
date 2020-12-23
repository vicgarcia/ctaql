from django.urls import path
from graphene_django.views import GraphQLView
from bustracker.schema import schema


urlpatterns = [

    # graphql endpoint
    path ('graphql/', GraphQLView.as_view(graphiql=True, schema=schema))

]
