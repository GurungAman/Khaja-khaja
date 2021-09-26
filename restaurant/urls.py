from django.urls import path
from . import views

urlpatterns = [
    path('restaurant/register/', views.register_restaurant, ),
    path('restaurant/<int:pk>', views.restaurant_detail, ),
    path('restaurant/', views.RestaurantList.as_view(), ),

    path('restaurant/food_items/category/', views.CategoryList.as_view(), ),
    path('restaurant/food_items/tags/', views.TagsList.as_view(), ),
    path('restaurant/food_items/', views.FoodItemsList.as_view(), ),
    path('restaurant/food_items/<int:pk>', views.FoodItemDetail.as_view(), ),
    path('restaurant/food_items/<int:pk>/discount/',
         views.DiscountView.as_view(), ),

]
