from django.db import models

# 'Category' represents a group of products.
# Think of it like a department in a store (e.g., "Electronics" or "Clothing").
# It helps us organize our catalog so users can find what they are looking for more easily.
class Category(models.Model):
    # 'name' is the title of the category.
    # It's like the sign above the department door.
    name = models.CharField(max_length=255)
    
    # 'description' gives more detail about what this category contains.
    # It's like the blurb in a catalog explaining what kind of items you'll find here.
    description = models.TextField(blank=True, null=True)

    # The __str__ method tells Django how to display this object in the admin panel.
    # It's like a name tag for the category.
    def __str__(self):
        return self.name
    # We add 's' after 'product' in the string to make it plural for the URL.
    # This allows the URL to be /catalog/products/, which is standard for a list endpoint.
    class Meta:
        verbose_name_plural = 'Categories'

# 'Product' is the main item we are selling.
# Think of it like a specific "design" or "model" of an item (e.g., "Classic Blue Jeans").
# Every product belongs to a specific category.
class Product(models.Model):
    # 'name' is the name of the product.
    # This is what customers will see first when browsing.
    name = models.CharField(max_length=255)
    
    # 'description' provides details about the product.
    # It's the "sales pitch" explaining the features and benefits of the item.
    description = models.TextField()
    
    # 'category' links this product to a specific Category.
    # We use a ForeignKey because many products can belong to one category.
    # 'on_delete=models.CASCADE' means if a category is deleted, all its products go with it.
    # It's like saying if a department closes, everything inside it is cleared out.
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)

    # Again, we return the name so the admin panel is easy to read.
    def __str__(self):
        return self.name

# 'ProductVariant' handles the different options for a product.
# Think of it like the specific items on the shelf.
# A "Classic Blue Jeans" product might have variants for "Size 32, Blue" or "Size 34, Blue".
# This is where the actual price and stock levels live.
class ProductVariant(models.Model):
    # 'product' links this variant back to the main Product.
    # Many variants (different sizes/colors) can belong to one product.
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    
    # 'size' represents the physical size of the variant (e.g., "Small", "Medium", "Large").
    # It's like the label on the collar of a shirt.
    size = models.CharField(max_length=50)
    
    # 'color' represents the color option (e.g., "Red", "Navy Blue", "Black").
    # It's what the customer picks to match their style.
    color = models.CharField(max_length=50)
    
    # 'price' is the cost of this specific variant.
    # We use DecimalField for accuracy when dealing with money.
    # 'max_digits=10' and 'decimal_places=2' allows for prices up to 99,999,999.99.
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # 'inventory_count' tracks how many of this specific item we have in the warehouse.
    # 'default=0' ensures we start with no stock until we add some.
    inventory_count = models.IntegerField(default=0)

    # We return a descriptive string combining the product name, size, and color.
    # This helps warehouse staff and admins identify the exact item at a glance.
    def __str__(self):
        return f"{self.product.name} - {self.size} ({self.color})"
