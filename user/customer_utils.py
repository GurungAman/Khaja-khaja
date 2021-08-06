from django.contrib.auth import get_user_model
from .models import Customer
from .serializers import CustomerSerializer

User = get_user_model()

def customer_details(email):
    customer = Customer.objects.get(customer__email = email)
    customer_serializer =  CustomerSerializer(customer)
    customer_data = customer_serializer.data
    return customer_data