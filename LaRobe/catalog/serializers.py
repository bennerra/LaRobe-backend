from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from rest_framework import serializers

from auth_server.models import User
from catalog.models import Product, Review


class ProductListSerializer(serializers.ModelSerializer):
    stock = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        avg_rating = obj.reviews.aggregate(Avg('rating'))
        return {
            "rating": avg_rating['rating__avg'] or 0,
            "count": obj.reviews.count()
        }

    def get_stock(self, obj):
        return obj.count > 0

    class Meta:
        model = Product

        fields = (
            "slug",
            "image",
            "title",
            "price",
            "stock",
            "rating"
        )


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product

        fields = (
            "description",
            "image",
            "price",
            "title",
            "brand",
            "count"
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()

    def get_author(self, obj):
        return {"username": obj.user.username, "id": obj.user.id}

    def get_product(self, obj):
        return {
            "title": obj.product.title,
            "slug": obj.product.slug
        }

    class Meta:
        model = Review
        fields = (
            "created_at",
            "details",
            "rating",
            "user_id",
            "author",
            "product"
        )

class ReviewCreateSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    product = serializers.SlugRelatedField(
        queryset=Product.objects.all(),
        slug_field='slug',
    )

    class Meta:
        model = Review
        fields = (
            "created_at",
            "details",
            "rating",
            "user",
            "product",
        )
