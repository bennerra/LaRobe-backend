from rest_framework import serializers

from catalog.models import Product


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product

        fields = (
            "slug",
            "image",
            "title",
            "price",
        )
