from django.urls import path, include

from catalog import views

name = "catalog"

urlpatterns = [
    path("products/", views.ProductViewSet.as_view({"get": "list"})),
    path("products/<slug:slug>/", views.ProductViewSet.as_view({"get": "retrieve"})),
    path("products/<slug:slug>/reviews", views.ReviewViewSet.as_view({"post": "create", "get": "list"})),
    path("users/<pk>/reviews", views.ReviewViewSet.as_view({"get": "list"})),
    path("reviews/", views.ReviewViewSet.as_view({"get": "list"})),
]