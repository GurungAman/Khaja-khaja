from restaurant.models import FoodItems
from .serializers import OrderItemSerializer


def order_details(order_instance):
    # order_instance parameter is a single queryset
    order = {}
    order['customer'] = order_instance.user.get_name
    order_items = order_instance.order_items.all()
    order['order_items'] = []
    for order_item in order_items:
        order_item_serializer = OrderItemSerializer(order_item)
        order_item_data = order_item_serializer.data
        print(order_item_data)
        food_item = FoodItems.objects.get(id=order_item_data['food_item'])
        order_item_data['food_item'] = food_item.name
        order_item_data.pop('user')
        order['order_items'].append(order_item_data)
    return order


def order_items_details(order_items):
    response = []
    for order_item in order_items:
        order_item_serializer = OrderItemSerializer(order_item)
        data = order_item_serializer.data
        food_item = FoodItems.objects.get(id=data['food_item'])
        data['food_item_name'] = food_item.name
        if food_item.image:
            data['food_item_logo'] = food_item.image
        response.append(data)
    return response
