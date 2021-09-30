import json
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .serializers import (
    CustomerSerializer, CreateBaseUserSerializer, UpdateCustomerSerializer
)
from .customer_utils import customer_details
from .models import Customer
from permissions import IsCustomerOnly
from tasks import verify_user_email


User = get_user_model()

# Create your views here.


@extend_schema(request=CustomerSerializer)
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
    try:
        json_str = request.body.decode('utf-8')
        user_data = json.loads(json_str)
        base_user_serializer = CreateBaseUserSerializer(
            data=user_data['base_user'])
        customer_serializer = CustomerSerializer(data=user_data)
        if customer_serializer.is_valid(raise_exception=False) \
                and base_user_serializer.is_valid(raise_exception=False):
            user = base_user_serializer.save(user_data['base_user'])
            data = customer_serializer.data
            customer_serializer.save(data)
            current_site = get_current_site(request)
            # verify_user_email.delay(
            #     user_id=user.id, domain=current_site.domain)
            response['data'] = customer_details(user.email)
            response['status'] = True
        else:
            response['errors'] = customer_serializer.errors
    except Exception as e:
        response['error'] = {f"{e.__class__.__name__}": f"{e}"}
    return Response(response)


class CustomerDetails(APIView):

    permission_classes = [IsCustomerOnly]

    def get(self, request):
        user = request.user
        response = {'status': False}
        try:
            customer = customer_details(email=user)
            response['user_details'] = customer
            response['status'] = True
        except Exception as e:
            response['error'] = {f"{e.__class__.__name__}": f"{e}"}
        return Response(response)

    @extend_schema(request=UpdateCustomerSerializer)
    def put(self, request):
        # {
        #     "primary_phone_number": "dfgdfg",
        #     "first_name": "test",
        #     "middle_name": "post",
        #     "last_name": "grgg",
        #     "address": "test123"
        # }
        user = request.user
        data = request.data
        response = {'status': False}
        try:
            customer = Customer.objects.get(customer=user)
            customer_serializer = UpdateCustomerSerializer(data=data)
            if customer_serializer.is_valid(raise_exception=False):
                customer_serializer.update(
                    instance=customer, validated_data=data)
                response['user_details'] = customer_details(
                    email=user.email)
                response['status'] = True
            else:
                response['error'] = customer_serializer.errors
        except Exception as e:
            response['error'] = f"{e.__class__.__name__ }"
        return Response(response)

    def delete(self, request):
        user = request.user
        response = {'status': False}
        try:
            customer = Customer.objects.get(customer=user)
            customer.is_active = False
            customer.save()
            response['status'] = True
        except Exception as e:
            response['error'] = {f"{e.__class__.__name__}": f"{e}"}
        return Response(response)
