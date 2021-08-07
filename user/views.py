import json
from django.contrib.auth import get_user_model
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CustomerSerializer, CreateBaseUserSerializer, UpdateCustomerSerializer
from .customer_utils import customer_details
from .models import Customer
from permissions import IsCustomerOnly

User = get_user_model()

# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def register_customer(request):
    # {
    #     "base_user": {
    #         "email": "new1@test.com",
    #         "primary_phone_number": "asdklfju",
    #         "password": "amangrg123",
    #         "password_1": "amangrg123"
    #     },
    #     "first_name": "test",
    #     "middle_name": "post",
    #     "last_name": "grgg",
    #     "address": "pkr"
    # }
    response = {
        'status': False
    }
    json_str = request.body.decode('utf-8')
    restaurant_data = json.loads(json_str)
    base_user_serializer = CreateBaseUserSerializer(data = restaurant_data['base_user'])
    customer_serializer = CustomerSerializer(data=restaurant_data)
    if customer_serializer.is_valid(raise_exception=False) and base_user_serializer.is_valid(raise_exception=False):
        base_user_serializer.save(restaurant_data['base_user'])
        data = customer_serializer.data
        customer_serializer.save(data)
        response['data'] = data
        response['status'] = True
    else:
        response['errors'] =  customer_serializer.errors
    return Response(response)


class CustomerDetails(APIView):

    permission_classes = [IsCustomerOnly]
    response = {
        'status': False
    }

    def get(self, request):
        user = request.user
        try:
            customer = customer_details(email = user)
            self.response['user_details'] = customer
            self.response['status'] = True
        except Exception as e:
            self.response['message'] = {
                'error': f"{e.__class__.__name__}"
            }
        return Response(self.response)

    def put(self, request):
        # {
        #     "email": "test@test.com",
        #     "primary_phone_number": "dfgdfg",
        #     "first_name": "test",
        #     "middle_name": "post",
        #     "last_name": "grgg",
        #     "address": "test123"
        # }
        user = request.user
        data = request.data
        try:
            customer = Customer.objects.get(customer__email = user.email)
            customer_serializer = UpdateCustomerSerializer(data=data)
            if customer_serializer.is_valid(raise_exception=True):
                customer.save()
                customer_serializer.update(instance = customer, validated_data=data)
                customer = customer_serializer.data
                self.response['user_details'] = customer
                self.response['status'] = True
        except Exception as e:
            self.response['message'] = {
                'error': f"{e.__class__.__name__}"
            }
        return Response(self.response)
    
    def delete(self, request):
        user = request.user
        try:
            customer = Customer.objects.get(customer__email = user.email)
            customer.is_active = False
            customer.save()
            self.response['status'] = True
        except Exception as e:
            self.response['message'] = {
                'error': f"{e.__class__.__name__}"
            }
        return Response(self.response)
