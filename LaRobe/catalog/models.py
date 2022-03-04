from django.db import models

from auth_server.models import User


class Product(models.Model):
    title = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products')
    count = models.IntegerField(default=0)


class Review(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    details = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.DecimalField(max_digits=5, decimal_places=2)
