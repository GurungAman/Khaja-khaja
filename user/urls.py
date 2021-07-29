from django.urls import path
from .views import *

urlpatterns = [
    path('customer/create', register_customer ),
]
