import json
from django.contrib.auth import get_user_model
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import CustomerSerializer, CreateBaseUserSerializer, UpdateCustomerSerializer
from .utils import customer_details, JWT_get_user
from .models import Customer

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
    customer_data = json.loads(json_str)
    base_user_serializer = CreateBaseUserSerializer(data = customer_data['base_user'])
    customer_serializer = CustomerSerializer(data=customer_data)
    if base_user_serializer.is_valid(raise_exception=True) and  customer_serializer.is_valid(raise_exception=True):            
        base_user_serializer.save()
        data = customer_serializer.data
        customer_serializer.save(data)
    response['data'] = data
    response['status'] = True
    return Response(response)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_customer_details(request):
    response = {
        'status': False
    }
    user = JWT_get_user(request=request)
    try:
        if user.is_customer:
            customer = customer_details(email = user)
            response['user_details'] = customer
        # if user.is_restaurant:
        response['status'] = True
    except Exception as e:
        response['message'] = {
            'error': f"{e.__class__.__name__}"
        }
    return Response(response)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_user(request):
    # {
    #     "email": "test@test.com",
    #     "primary_phone_number": "dfgdfg",
    #     "first_name": "test",
    #     "middle_name": "post",
    #     "last_name": "grgg",
    #     "address": "test123"
    # }
    response = {
        'status': False
    }
    user = JWT_get_user(request=request)
    json_str = request.body.decode('utf-8')
    data = json.loads(json_str)
    try:
        if user.is_customer:
            customer = Customer.objects.get(customer__email = user.email)
            customer_serializer = UpdateCustomerSerializer(data=data)
            if customer_serializer.is_valid(raise_exception=True):
                customer.save()
                customer_serializer.update(instance = customer, validated_data=data)
                customer = customer_serializer.data
                response['user_details'] = customer
            response['status'] = True
    except Exception as e:
        response['message'] = {
            'error': f"{e.__class__.__name__}"
        }
    return Response(response)
