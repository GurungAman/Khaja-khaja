from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
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
        food_item = FoodItems.objects.get(id=validated_data['food_item'])
        customer = Customer.objects.get(id=validated_data['user'])
        order_item, created = OrderItem.objects.get_or_create(
            user=customer,
            food_item=food_item,
            ordered=False
        )
        order_item.quantity = validated_data['quantity']
        order_item.save()
        return order_item


class OrderSerializer(serializers.ModelSerializer):
    shipping_address = serializers.CharField(required=False)
    order_items = serializers.CharField(required=False)

    class Meta:
        model = Order
        fields = "__all__"

    def save(self, validated_data):
        customer = Customer.objects.get(id=validated_data['user'])
        address = customer.address
        if validated_data.get('shipping_address'):
            address = validated_data['shipping_address']
        order, _ = Order.objects.get_or_create(
            user=customer,
            shipping_address=address,
            order_status=None
        )
        order_items = OrderItem.objects.filter(user=customer, ordered=False)
        if not order_items.exists():
            raise ValidationError("Empty cart")
        for order_item in order_items:
            if order_item.user == customer:
                order.order_items.add(order_item)
            else:
                raise PermissionError("You do not own this order item.")
        return order
