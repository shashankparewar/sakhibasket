from django.contrib import admin

from .models import Order, Category, Item, OrderItem

admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Item)
admin.site.register(OrderItem)