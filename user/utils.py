import json

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication


from .models import Customer
from .serializers import  CustomerSerializer

User = get_user_model()

def customer_details(email):
    customer = Customer.objects.get(customer__email = email)
    customer_serializer =  CustomerSerializer(customer)
    # converts data into json format/type
    customer_data = json.loads(json.dumps(customer_serializer.data))
    return customer_data

def JWT_get_user(request):
    try:
        user, _ = JWTAuthentication().authenticate(request)
        return user
    except:
        return None
