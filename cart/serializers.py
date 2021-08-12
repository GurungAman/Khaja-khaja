from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Discount, OrderItem, Order
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
    DISCOUNT_TYPES = (
        ('percentage', 'Percentage'),
        ('amount', 'Amount')
    )    
    discount_type = serializers.ChoiceField(choices=DISCOUNT_TYPES, required=False)
    discount_amount = serializers.DecimalField(max_digits=8, decimal_places=2, required=False)

    class Meta:
        model = Order
        fields = ['id', 'user', 'order_items',
                  'shipping_address', 'discount_type', 'discount_amount']

    def save(self, validated_data):
        discount_data = validated_data.get('discount_data')
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
        if discount_data:
            discount = Discount.objects.create(
                order = order,
                discount=discount_data['discount_amount'],
                discount_type=discount_data['discount_type'],
            )
        return order
