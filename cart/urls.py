from django.urls import path
from . import views

urlpatterns = [
    path('customer/order-item/', views.OrderItemDetail.as_view(), ),
    path('customer/order/', views.OrderDetail.as_view(), ),
    path('order/checkout/', views.checkout, ),

]
