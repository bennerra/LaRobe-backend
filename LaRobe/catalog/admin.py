from django.contrib import admin
from unfold.admin import ModelAdmin

from catalog.models import Product


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    def has_module_permission(self, request):
        return True

    def has_view_permission(self, request, obj = ...):
        return True

    def has_add_permission(self, request):
        return True