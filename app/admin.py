from django.contrib import admin
from .models import (
    Customer, 
    Product, 
    Cart, 
    OrderPlaced
)

# Register Customer model
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality', 'city', 'zipcode', 'state']

# Register Product model
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'discounted_price', 'selling_price', 'description', 'brand', 'category', 'product_image']

# Register Cart model
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']

# Register OrderPlaced model
@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product','quantity', 'ordered_date', 'status']

