from django.urls import path
from . import views

urlpatterns = [
    path('customer/order_item/', views.OrderItemDetail.as_view(), ),
    path('customer/order/', views.OrderDetail.as_view(), ),
]
