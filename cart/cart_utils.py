from django.contrib.auth import get_user_model
from user.models import Customer
from restaurant.models import FoodItems
from .models import OrderItem, Order
from .serializers import OrderItemSerializer

def order_details(order):
    customer = Customer.objects.get(id = order['user'])
    order['customer'] = customer.get_name
    order_items = order['order_items']
    order['order_items'] = []
    for i in order_items:
        item = OrderItem.objects.get(id=i)
        order_item_serializer = OrderItemSerializer(item)
        order_item_data = order_item_serializer.data
        food_item = FoodItems.objects.get(id=order_item_data['food_item'])
        order_item_data['food_item'] = food_item.name
        order_item_data.pop('user')
        order['order_items'].append(order_item_data)
    order['total_cost'] = 0
    return order
