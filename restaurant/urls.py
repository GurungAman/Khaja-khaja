from django.urls import path
from .views import *

urlpatterns = [
    path('restaurant/category/', CategoryList.as_view(), ),
    path('restaurant/tags/', TagsList.as_view(), ),
    path('restaurant/menu/', MenuList.as_view(), ),
    
    path('restaurant/food_items/', FoodItemsList.as_view(), ),
    path('restaurant/food_items/<int:pk>', FoodItemDetail.as_view(), ),



]
