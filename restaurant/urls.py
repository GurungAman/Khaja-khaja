from django.urls import path
from .views import *

urlpatterns = [
    path('restaurant/category/', CategoryList.as_view(), ),

]
