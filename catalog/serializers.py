from rest_framework import serializers
from .models import Category, Product, ProductVariant

# 'CategorySerializer' acts like a translator.
# It takes our Category database objects and turns them into JSON format,
# which is a universal language that frontend apps (like websites or mobile apps) understand.
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        # We tell the serializer which model it is translating.
        model = Category
        # We specify which fields to include in the JSON.
        # '__all__' is a shortcut to include every field in the model.
        fields = '__all__'

# 'ProductSerializer' translates our Product items.
# It also helps us show information from related models.
class ProductSerializer(serializers.ModelSerializer):
    # 'category_name' is a special "shortcut" field.
    # Normally, Django only gives us the category ID number. 
    # This line tells the serializer to reach into the related category and grab its actual name instead.
    # It's like having a label that says "Clothing" instead of just "Category #1".
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Product
        # We list out the specific fields we want to show in the API.
        fields = ['id', 'name', 'description', 'category', 'category_name']

# 'ProductVariantSerializer' is where the magic happens.
# This handles the specific items (like a "Red Medium T-Shirt") and enforces our shop's rules.
class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'
        
        # 'read_only_fields' are like "view-only" files in a shared folder.
        # We want users to see the inventory count, but we don't want them to be able to change it
        # by sending a fake number in their API request.
        # Only our warehouse logic (or an admin) should be able to update stock.
        read_only_fields = ['inventory_count']

    # Custom validation is like a security guard standing at the door.
    # Whenever someone tries to save a new price, this method checks if the price follows our rules.
    def validate_price(self, value):
        # We check if the price is a negative number.
        # You can't pay someone to take your products!
        if value < 0:
            # If the price is negative, we sound the alarm by raising a ValidationError.
            # This stops the process and sends a clear message back to the user.
            raise serializers.ValidationError("Price cannot be negative. Even a clearance sale has to cost at least $0!")
        
        # If the price is $0 or more, the guard waves them through.
        return value
