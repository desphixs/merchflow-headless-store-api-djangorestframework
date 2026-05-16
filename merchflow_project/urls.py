from django.contrib import admin
from django.urls import path, include

# The project's main 'urls.py' is like the central lobby of our building.
# Instead of listing every single room here, we point users toward the correct "department" switchboards.

urlpatterns = [
    # The admin dashboard remains at its own dedicated path.
    path('admin/', admin.site.urls),
    
    # We use 'include' to connect our 'catalog' app's internal switchboard.
    # Every URL defined in 'catalog/urls.py' will now start with 'api/'.
    # This keeps our main file clean and makes our API easy to manage as it grows.
    path('api/', include('catalog.urls')),
]
