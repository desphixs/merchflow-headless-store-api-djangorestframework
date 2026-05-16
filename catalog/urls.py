from django.urls import path
from . import views

# This file is the dedicated switchboard for our 'catalog' app.
# By keeping catalog URLs here, we keep our project organized and clean.
# It's like having a specific directory for the "Catalog Department" in a large office building.

urlpatterns = [
    # --- Category Endpoints ---
    
    # This path handles requests for the full list of categories.
    # When a user goes to /api/categories/, we send them to our 'CategoryList' view.
    path('categories/', views.CategoryList.as_view(), name='category-list'),
    
    # This path handles requests for a specific category using its ID number.
    path('categories/<int:pk>/', views.CategoryDetail.as_view(), name='category-detail'),

    # --- Product Endpoints ---

    # This path handles requests for the full catalog of products.
    # Browsing /api/products/ will trigger our 'ProductList' view.
    path('products/', views.ProductList.as_view(), name='product-list'),

    # This path allows users to interact with a specific product design.
    # For example, /api/products/12/ would target the product with ID 12.
    path('products/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),

    # --- Product Variant Endpoints ---

    # This path handles the full inventory of product variations.
    # Visit /api/variants/ to see everything in the warehouse.
    path('variants/', views.ProductVariantList.as_view(), name='variant-list'),

    # This path targets one specific variant in our warehouse.
    # Use /api/variants/8/ to update the details of variation #8.
    path('variants/<int:pk>/', views.ProductVariantDetail.as_view(), name='variant-detail'),
]
