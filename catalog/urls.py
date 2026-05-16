from django.urls import path
from . import views

# This file is the dedicated switchboard for our 'catalog' app.
# By keeping catalog URLs here, we keep our project organized and clean.
# It's like having a specific directory for the "Catalog Department" in a large office building.

urlpatterns = [
    # This path handles requests for the full list of categories.
    # When a user goes to /api/categories/, we send them to our 'CategoryList' view.
    # '.as_view()' is a special instruction that tells Django to treat our class like a view function.
    path('categories/', views.CategoryList.as_view(), name='category-list'),
    
    # This path handles requests for a specific category using its ID number.
    # '<int:pk>' is like a variable in the URL. 
    # If the user goes to /api/categories/5/, Django knows they are looking for category #5.
    path('categories/<int:pk>/', views.CategoryDetail.as_view(), name='category-detail'),
]
