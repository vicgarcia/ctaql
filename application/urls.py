from django.urls import path, include
from django.conf.urls import url

from core import views as core_views
from account import views as account_views

urlpatterns = [

    # health check endpoint
    path('health/', core_views.HealthCheckView.as_view()),

    # account management endpoints
    path('token/', account_views.LoginView.as_view()),
    path('profile/', account_views.ProfileView.as_view()),


]
