from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category
from .serializers import CategorySerializer

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
