from django.contrib import admin
from .models import Category, Product, ProductVariant

# Registering our models so they show up in the Django Admin panel.
# This allows us to manage our data through a nice web interface instead of just the database.

# 'CategoryAdmin' lets us customize how Categories are displayed and edited.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # 'list_display' tells Django which fields to show in the list view.
    list_display = ('name', 'description')

# 'ProductAdmin' manages the main Product listings.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # We show the name and the category it belongs to.
    list_display = ('name', 'category')
    # 'list_filter' adds a sidebar to filter products by their category.
    list_filter = ('category',)

# 'ProductVariantAdmin' manages the specific versions (sizes/colors) of products.
@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    # We show all the important info: which product it is, size, color, price, and stock.
    list_display = ('product', 'size', 'color', 'price', 'inventory_count')
    # We allow filtering by product to make it easier to find variants.
    list_filter = ('product', 'size', 'color')
