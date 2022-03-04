from rest_framework import viewsets, status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from catalog.models import Product, Review
from catalog.serializers import ProductListSerializer, ProductDetailSerializer, ReviewSerializer, ReviewCreateSerializer
from auth_server import permissions
from rest_framework import exceptions


class ProductViewSet(viewsets.ModelViewSet):
    PERMISSION_CLASSES = (
        permissions.NotBlocked
    )
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        if self.action == "retrieve":
            return ProductDetailSerializer
        return super(self).get_serializer_class()

    def get_queryset(self):
        if self.action == "retrieve":
            return Product.objects.all()

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


class ReviewViewSet(viewsets.ModelViewSet):
    PERMISSION_CLASSES = (
        permissions.NotBlocked
    )
    pagination_class = None

    def get_serializer_class(self):
        if self.action == "list":
            return ReviewSerializer

        if self.action == "create":
            return ReviewCreateSerializer

        return super(self).get_serializer_class()

    def get_queryset(self):
        if self.kwargs.get("slug"):
            return Review.objects.filter(product__slug=self.kwargs.get("slug"))
        if self.kwargs.get("pk"):
            return Review.objects.filter(user_id=self.kwargs.get("pk"))
        raise APIException({"detail": "Not found."})

    def create(self, request, *args, **kwargs):
        data = {
            **request.data.dict(),
            "user": request.user.id,
            "product": self.kwargs.get("slug"),
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
