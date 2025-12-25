from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from auth_server import views

name = "auth_server"

urlpatterns = [
    path("signup/", views.RegistrationViewSet.as_view({"post": "create"})),
    path("signin/", obtain_auth_token),
    path("profile/", views.ProfileViewSet.as_view({"get": "retrieve"})),
]