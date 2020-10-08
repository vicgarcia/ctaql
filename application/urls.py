from django.urls import path, include
from django.conf.urls import url
from core import views as core_views
from users import views as users_views
from bustracker import views as bustracker_views

urlpatterns = [

    # health check endpoint
    path('health/', core_views.HealthCheckView.as_view()),

    # account management endpoints
    path('token/', users_views.LoginView.as_view()),
    path('profile/', users_views.ProfileView.as_view()),

    # graphql endpoint
    path('graphql/', bustracker_views.AuthenticatedGraphQLView.as_view())

]
