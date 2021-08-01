from django.urls import path
from .views import *

urlpatterns = [
    path('customer/create/', register_customer, ),
    path('customer/get/', get_customer_details, ),
    path('customer/update/', update_user, ),

]
