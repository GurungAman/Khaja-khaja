from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderItemSerializer, OrderSerializer
from permissions import IsCustomerOnly
from .cart_utils import order_details, order_items_details

# Create your views here.


class OrderItemDetail(APIView):
    response = {
        'status': False
    }
    permission_classes = [IsCustomerOnly]

    def get(self, request):
        user = request.user.customer
        try:
            order_items = OrderItem.objects.filter(user=user, ordered=False)
            order_item_detail = order_items_details(order_items)
            self.response['status'] = True
            self.response['order_items'] = order_item_detail
        except Exception as e:
            self.response['error'] = {
                f"{e.__class__.__name__}": f"{e}"
            }
        return Response(self.response)

    def post(self, request):
        """
        {
            "food_item": 5,
            "quantity": 3
        }
        """
        data = request.data
        data['user'] = request.user.customer.pk
        try:
            order_item = OrderItemSerializer(data=data)
            if order_item.is_valid(raise_exception=False):
                order_items = order_item.save(validated_data=data)
                self.response['status'] = True
                self.response['order_item'] = order_items_details(
                    [order_items])
            else:
                self.response['error'] = order_item.errors
        except Exception as e:
            self.response['error'] = {
                f"{e.__class__.__name__}": f"{e}"
            }
        return Response(self.response)


class OrderDetail(APIView):
    response = {
        'status': False
    }
    permission_classes = [IsCustomerOnly]

    def get(self, request):
        user = request.user.customer
        try:
            order = Order.objects.filter(
                user=user,
                order_status=None
            )
            if not order.exists():
                self.response['order_item'] = "You have not \
                                                made any orders yet"
            else:
                self.response['order_item'] = order_details(order[0])
                self.response['status'] = True
        except Exception as e:
            self.response['error'] = {
                f"{e.__class__.__name__}": f"{e}"
            }
        return Response(self.response)

    def post(self, request):
        data = request.data
        data['user'] = request.user.customer.pk
        try:
            order_serializer = OrderSerializer(data=data)
            if order_serializer.is_valid(raise_exception=False):
                order = order_serializer.save(validated_data=data)
                self.response['status'] = True
                self.response['order'] = order_details(order)
                self.response['order']['total_cost'] = order.total_cost
            else:
                self.response['error'] = order_serializer.errors
        except Exception as e:
            self.response['error'] = {
                f"{e.__class__.__name__}": f"{e}"
            }
        return Response(self.response)

    def delete(self, request):
        data = request.data
        user = request.user.customer
        try:
            order = Order.objects.get(id=data['order_id'])
            if user != order.user:
                raise PermissionError("Permission denied.")
            order.delete()
            self.response['status'] = True
        except Exception as e:
            self.response['error'] = {
                f"{e.__class__.__name__}": f"{e}"
            }
        return Response(self.response)
