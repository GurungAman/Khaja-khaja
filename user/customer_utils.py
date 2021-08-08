from django.contrib.auth import get_user_model
from .models import Customer
from .serializers import CustomerSerializer

User = get_user_model()

def customer_details(email):
    customer = Customer.objects.get(customer__email = email)
    customer_serializer =  CustomerSerializer(customer)
    customer_data = customer_serializer.data
    base_user = customer_data.pop('base_user')
    customer_data['email'] = base_user['email']
    customer_data['primary_phone_number'] = base_user.get('primary_phone_number')
    return customer_data