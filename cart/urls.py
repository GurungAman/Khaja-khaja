from django.urls import path
from .views import *

urlpatterns = [
    path('customer/order_item/', OrderItemDetail.as_view(), ),
    path('customer/order/', OrderDetail.as_view(), ),
]
