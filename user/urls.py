from django.urls import path
from .views import *

urlpatterns = [
    path('customer/register/', register_customer, ),

    path('customer/', CustomerDetails.as_view(),)

]
