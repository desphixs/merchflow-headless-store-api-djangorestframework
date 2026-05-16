from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

# --- Category Views ---

# 'CategoryList' handles requests for the entire collection of categories.
# It's like the main reception desk at the store where you can ask to see all departments
# or request to open a brand new one.
class CategoryList(APIView):
    # 'get' is for retrieving data. 
    # This is like a customer walking up and asking, "Can I see a list of all your departments?"
    def get(self, request):
        # We grab every category record from our database.
        categories = Category.objects.all()
        # We hand the list to our serializer (the translator) to turn it into JSON.
        # 'many=True' tells it that we are sending a list of items, not just one.
        serializer = CategorySerializer(categories, many=True)
        # We send the translated JSON back to the user with a "200 OK" status.
        return Response(serializer.data)

    # 'post' is for creating new data.
    # This is like a manager submitting a form to create a new department.
    def post(self, request):
        # We take the JSON data the user sent us and hand it to the serializer.
        serializer = CategorySerializer(data=request.data)
        # The serializer (the bouncer) checks if the data is valid (e.g., if the name isn't blank).
        if serializer.is_valid():
            # If everything looks good, we save the new category to the database.
            serializer.save()
            # we return the new data and a "201 Created" status to confirm success.
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # If the data is bad, we return the errors and a "400 Bad Request" status.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 'CategoryDetail' handles requests for one specific category.
# It's like walking directly into one specific room (e.g., the "Clothing" department)
# to look around, change the sign, or close it down entirely.
class CategoryDetail(APIView):
    # This helper method is like a security check.
    # It tries to find the specific category using its unique ID (pk).
    def get_object(self, pk):
        try:
            # We look for the category in the database.
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            # If the ID doesn't exist, we raise a 404 error (Not Found).
            # It's like trying to walk into a room that doesn't exist in the building.
            raise Http404

    # 'get' retrieves one specific category.
    def get(self, request, pk):
        # We find the object first using our helper.
        category = self.get_object(pk)
        # We translate that single object into JSON.
        serializer = CategorySerializer(category)
        # We send the data back to the user.
        return Response(serializer.data)

    # 'put' is for updating an existing category.
    # It's like repainting the walls or changing the description of a department.
    def put(self, request, pk):
        # Find the category first.
        category = self.get_object(pk)
        # Hand the existing category AND the new data to the serializer.
        serializer = CategorySerializer(category, data=request.data)
        # The bouncer checks the new data.
        if serializer.is_valid():
            # If valid, update the record in the database.
            serializer.save()
            # Return the updated data.
            return Response(serializer.data)
        # Return errors if the data is bad.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 'delete' is for removing a category.
    # This is like permanently closing a department and clearing out the space.
    def delete(self, request, pk):
        # Find the category first.
        category = self.get_object(pk)
        # Remove it from the database.
        category.delete()
        # Return a "204 No Content" status to show it's gone and there's nothing left to show.
        return Response(status=status.HTTP_204_NO_CONTENT)


# --- Product Views ---

# 'ProductList' works just like CategoryList, but for our inventory of products.
# It's the catalog desk where you can browse every product we sell or add a new design to the shelves.
class ProductList(APIView):
    # 'get' returns all products currently in our system.
    def get(self, request):
        # We fetch every single product record.
        products = Product.objects.all()
        # We translate the list of products into JSON.
        serializer = ProductSerializer(products, many=True)
        # Send the data back with a success status.
        return Response(serializer.data)

    # 'post' allows us to add a brand new product to our catalog.
    def post(self, request):
        # We hand the incoming product details to our translator.
        serializer = ProductSerializer(data=request.data)
        # The serializer checks if the product has a name, description, and valid category.
        if serializer.is_valid():
            # If everything is correct, we save it to the database.
            serializer.save()
            # Confirm success with a "201 Created" message.
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # If something is missing or wrong, we let the user know.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 'ProductDetail' is the door to one specific product's data.
# Whether you need to check the details of a "Denim Jacket" or update its description, this is where you go.
class ProductDetail(APIView):
    # This helper method ensures the product exists before we try to do anything with it.
    def get_object(self, pk):
        try:
            # Try to find the product by its ID.
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            # If it's missing, we raise the 404 "Not Found" alarm.
            raise Http404

    # 'get' retrieves the details for one specific product.
    def get(self, request, pk):
        # Find the product.
        product = self.get_object(pk)
        # Translate it to JSON.
        serializer = ProductSerializer(product)
        # Send it back to the user.
        return Response(serializer.data)

    # 'put' lets us update the information for a specific product.
    # Maybe the design changed or we want to move it to a different category.
    def put(self, request, pk):
        # Find the product we want to edit.
        product = self.get_object(pk)
        # Hand the old record and the new data to the serializer.
        serializer = ProductSerializer(product, data=request.data)
        # Check if the updates are valid.
        if serializer.is_valid():
            # Save the changes.
            serializer.save()
            # Return the updated product info.
            return Response(serializer.data)
        # Return error details if the update failed validation.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 'delete' removes the product design from our system forever.
    def delete(self, request, pk):
        # Find the product.
        product = self.get_object(pk)
        # Remove it from the database.
        product.delete()
        # Return a "204 No Content" status to show the deletion was successful.
        return Response(status=status.HTTP_204_NO_CONTENT)
