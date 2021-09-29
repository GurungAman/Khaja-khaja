from restaurant.models import FoodItems
from .serializers import OrderItemSerializer


def order_items_details(order_items):
    response = []
    for order_item in order_items:
        order_item_serializer = OrderItemSerializer(order_item)
        data = order_item_serializer.data
        food_item = FoodItems.objects.get(id=data['food_item'])
        data['food_item_price'] = food_item.price
        data['food_item_name'] = food_item.name
        if food_item.image:
            data['food_item_logo'] = food_item.image
        response.append(data)
    return response


def order_details(order_instance):
    # order_instance parameter is a single queryset
    order = {}
    order['customer'] = order_instance.user.get_name
    order_items = order_instance.order_items.all()
    order['count_items'] = order_items.count()
    order['total_cost'] = order_instance.total_cost
    order['order_item_data'] = order_items_details(order_items)
    return order
