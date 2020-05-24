"""
Serializer File
"""
from rest_framework import serializers

from .models import Category, Item, Order, OrderItem, Address


class CategorySerializer(serializers.ModelSerializer):
    """
    Category Serializer Class
    """
    class Meta:
        """
        Category Serializer Meta Class
        """
        model = Category
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    """
    Item Serializer Class
    """
    class Meta:
        """
        Item Serializer Meta Class
        """
        model = Item
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    """
    Order Serializer Class
    """
    item = ItemSerializer()
    class Meta:
        """
        Item Serializer Meta Class
        """
        model = OrderItem
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    """
    Order Serializer Class
    """
    class Meta:
        """
        Item Serializer Meta Class
        """
        model = Address
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    """
    Order Serializer Class
    """
    items = OrderItemSerializer(many=True)
    shipping_address = AddressSerializer()
    class Meta:
        """
        Item Serializer Meta Class
        """
        model = Order
        fields = '__all__'