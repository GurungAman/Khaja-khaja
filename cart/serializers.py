from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import OrderItem
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
        order_item, _ = OrderItem.objects.get_or_create(
            user=customer,
            food_item=food_item,
            ordered=False
        )
        order_item.quantity = validated_data['quantity']
        order_item.save()
        return order_item
