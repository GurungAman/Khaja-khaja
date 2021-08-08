from django.urls import path
from .views import *

urlpatterns = [
    path('restaurant/register/', register_restaurant, ),
    path('restaurant/', RestaurantList.as_view(), ),

    path('restaurant/menu/', MenuList.as_view(), ),

    path('restaurant/food_items/category/', CategoryList.as_view(), ),
    path('restaurant/food_items/tags/', TagsList.as_view(), ),    
    path('restaurant/food_items/', FoodItemsList.as_view(), ),
    path('restaurant/food_items/<int:pk>', FoodItemDetail.as_view(), ),

]
