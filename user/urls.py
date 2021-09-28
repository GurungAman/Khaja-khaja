from django.urls import path
from . import views

urlpatterns = [
    path('customer/register/', views.register_customer, ),

    path('customer/', views.CustomerDetails.as_view(), ),

]
