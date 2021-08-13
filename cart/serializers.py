from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import OrderItem, Order
from restaurant.models import FoodItems
from user.models import Customer

User = get_user_model()

class OrderItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OrderItem
        fields = '__all__'

    def save(self, validated_data):
        food_item  = FoodItems.objects.get(id = validated_data['food_item'])
        customer = Customer.objects.get(id = validated_data['user'])
        order_item = OrderItem.objects.create(
            user = customer,
            food_item = food_item,
            quantity = validated_data['quantity'],
        )
        return order_item


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"

    def save(self, validated_data):
        customer = Customer.objects.get(id=validated_data['user'])
        address = customer.address
        if validated_data.get('shipping_address'):
            address = validated_data['shipping_address']
        order = Order.objects.create(
            user = customer,
            shipping_address = address,
        )
        for order_item in validated_data['order_items']:
                item = OrderItem.objects.get(id = order_item)
                order.order_items.add(item)
        return order
