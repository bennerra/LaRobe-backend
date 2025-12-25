from rest_framework import viewsets

from catalog.models import Product
from catalog.serializers import ProductListSerializer
from auth_server import permissions

class ProductViewSet(viewsets.ModelViewSet):
    PERMISSION_CLASSES = (
        permissions.NotBlocked
    )
    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        return None

    def get_queryset(self):
        filters = self.request.query_params
        applied_filters = {}
        if filters.get("stock") is not None:
            applied_filters["count__gte"] = 1

        if filters.get("not_stock") is not None:
            applied_filters["count"] = 0

        if filters.get("price__gte") is not None:
            applied_filters["price__gte"] = filters["price__gte"]

        if filters.get("price__lte") is not None:
            applied_filters["price__lte"] = filters["price__lte"]

        if filters.get("brands") is not None:
            applied_filters["brands__in"] = filters["brands"].split(",")

        return Product.objects.filter(**applied_filters)

