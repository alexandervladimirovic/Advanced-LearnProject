from django.contrib import admin
from django.http import HttpRequest

from .models import Category, Product


admin.site.site_header = 'Магазин BIG CORP'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug')
    ordering = ('name',)
    search_fields = ('name',)


    def get_prepopulated_fields(self, request, object=None):
        return {
            'slug': ('name',),
        }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'slug', 'price', 'available', 'created_at', 'updated_at')
    list_filter = ('available', 'created_at', 'updated_at')
    search_fields = ('title',)

    def get_prepopulated_fields(self, request, object=None):
        return {
            'slug': ('title',),
        }