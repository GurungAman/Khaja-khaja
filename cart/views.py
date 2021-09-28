from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderItemSerializer, OrderSerializer
from permissions import IsCustomerOnly
from .cart_utils import order_details, order_items_details

# Create your views here.


class OrderItemDetail(APIView):
    permission_classes = [IsCustomerOnly]

    def get(self, request):
        response = {'status': False}
        user = request.user.customer
        try:
            order_items = OrderItem.objects.filter(user=user, ordered=False)
            order_item_detail = order_items_details(order_items)
            response['status'] = True
            response['order_items'] = order_item_detail
        except Exception as e:
            response['error'] = {
                f"{e.__class__.__name__}": f"{e}"
            }
        return Response(response)

    def post(self, request):
        """
        {
            "food_item": 5,
            "quantity": 3
        }
        """
        response = {'status': False}
        data = request.data
        data['user'] = request.user.customer.pk
        try:
            order_item = OrderItemSerializer(data=data)
            if order_item.is_valid(raise_exception=False):
                order_items = order_item.save(validated_data=data)
                response['status'] = True
                response['order_item'] = order_items_details(
                    [order_items])
            else:
                response['error'] = order_item.errors
        except Exception as e:
            response['error'] = {
                f"{e.__class__.__name__}": f"{e}"
            }
        return Response(response)

    def delete(self, request):
        response = {'status': False}
        data = request.data
        user = request.user.customer
        try:
            for order_item_id in data['order_items_ids']:
                order_item = OrderItem.objects.get(id=order_item_id)
                if user != order_item.user:
                    raise PermissionError("Permission denied.")
                order_item.delete()
            response['status'] = True
        except Exception as e:
            response['error'] = {
                f"{e.__class__.__name__}": f"{e}"
            }
        return Response(response)


class OrderDetail(APIView):
    permission_classes = [IsCustomerOnly]

    def get(self, request):
        response = {'status': False}
        user = request.user.customer
        try:
            order = Order.objects.filter(
                user=user,
                order_status=None
            )
            if not order.exists():
                response['order_detail'] = "You have not " \
                    "made any orders yet"
            else:
                response['order_detail'] = order_details(order[0])
                response['status'] = True
        except Exception as e:
            response['error'] = {
                f"{e.__class__.__name__}": f"{e}"
            }
        return Response(response)

    def post(self, request):
        response = {'status': False}
        data = request.data
        data['user'] = request.user.customer.pk
        try:
            order_serializer = OrderSerializer(data=data)
            if order_serializer.is_valid(raise_exception=False):
                order = order_serializer.save(validated_data=data)
                response['status'] = True
                response['order'] = order_details(order)
            else:
                response['error'] = order_serializer.errors
        except Exception as e:
            response['error'] = {
                f"{e.__class__.__name__}": f"{e}"
            }
        return Response(response)

    def delete(self, request):
        response = {'status': False}
        user = request.user.customer
        try:
            order = Order.objects.get(
                user=user,
                order_status=None)
            order.delete()
            response['status'] = True
        except Exception as e:
            response['error'] = {
                f"{e.__class__.__name__}": f"{e}"
            }
        return Response(response)
