from django.contrib.auth import get_user_model

from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import CustomerSerializer, CustomUserSerializer

import json

User = get_user_model()

# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def register_customer(request):
    response = {
        'status': False
    }
    json_str = request.body.decode('utf-8')
    customer_data = json.loads(json_str)
    custom_user_serializer = CustomUserSerializer(data = customer_data['custom_user'])
    customer_serializer = CustomerSerializer(data=customer_data)
    if custom_user_serializer.is_valid(raise_exception=True) and  customer_serializer.is_valid(raise_exception=True):            
        custom_user_serializer.save()
        data = customer_serializer.data
        customer_serializer.save(data)
    response['data'] = data
    response['status'] = True
    return Response(response)

