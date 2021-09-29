from .serializers import NotificationsSerializer
from cart.models import OrderItem


def notification_details(notifications):
    data = []
    for notification in notifications:
        serializer = NotificationsSerializer(notification)
        response = serializer.data
        order_item = OrderItem.objects.get(id=notification.order_item.id)
        response['food_item_name'] = order_item.food_item.name
        response['quantity'] = order_item.quantity
        response['customer_name'] = order_item.user.get_name
        response.pop('user')
        response.pop('order_item')
        data.append(response)
    return data
