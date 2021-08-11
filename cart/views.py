import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from permissions import IsCustomerOnly
from .cart_utils import order_details


# Create your views here.

class OrderItemDetail(APIView):
    response = {
        'status': False
        }
    permission_classes = [IsCustomerOnly]

    def post(self, request):
        data = request.data
        data['user'] = request.user.pk
        try:
            order_item = OrderItemSerializer(data = data)
            if order_item.is_valid(raise_exception=False):
                order_item.save(validated_data = data)
                self.response['status'] = True
                self.response['order_item'] = order_item.data
            else:
                self.response['error'] = order_item.errors
        except Exception as e:
            self.response['error'] = f"{e.__class__.__name__}"
        return Response(self.response)


class OrderDetail(APIView):
    response = {
        'status': False
        }
    permission_classes = [IsCustomerOnly]

    def post(self, request):
        data = request.data
        data['user'] = request.user.pk
        try:
            order_serializer = OrderSerializer(data = data)           
            if order_serializer.is_valid(raise_exception=True):
                order = order_serializer.save(validated_data=data)
                self.response['status'] = True
                self.response['order'] = order_details(order_serializer.data)
                self.response['order']['total_cost'] = order.total_cost                
            else:
                self.response['error'] = order_serializer.errors
        except Exception as e:
            self.response['error'] = f"{e}"
        return Response(self.response)
