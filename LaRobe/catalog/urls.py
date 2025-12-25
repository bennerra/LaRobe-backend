from django.urls import path, include

from catalog import views

name = "catalog"

urlpatterns = [
    path("products/", views.ProductViewSet.as_view({"get": "list"}))
]